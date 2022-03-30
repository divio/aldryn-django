import os
import subprocess
import sys

from django.conf import settings as django_settings

import click
import furl
from aldryn_addons.utils import boolean_ish


# add the current directory to pythonpath. So the project files can be read.
BASE_DIR = os.getcwd()
sys.path.insert(0, BASE_DIR)


@click.command()
@click.pass_obj
def web(ctx_obj):
    """
    launch the webserver of choice (uwsgi)
    """
    execute(start_uwsgi_command(settings=ctx_obj['settings'], port=80))


@click.command()
@click.pass_obj
def migrate(ctx_obj):
    """
    run any migrations needed at deploy time. most notably database migrations.
    """
    cmds = ctx_obj['settings']['MIGRATION_COMMANDS']
    click.echo('aldryn-django: running migration commands')
    for cmd in cmds:
        click.echo(f'    ----> {cmd}')
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as exc:
            sys.exit(exc.returncode)


@click.group()
@click.option('--verbose', is_flag=True)
@click.pass_context
def main(ctx, verbose):
    if not os.path.exists(os.path.join(BASE_DIR, 'manage.py')):
        raise click.UsageError(
            'make sure you are in the same directory as manage.py'
        )

    if verbose:
        os.environ['ALDRYN_ADDONS_DEBUG'] = 'True'

    from . import startup
    startup._setup(BASE_DIR)

    ctx.obj = {
        'settings': {
            key: getattr(django_settings, key)
            for key in dir(django_settings)
        }
    }


main.add_command(web)
main.add_command(migrate)


def get_env():
    # setup default uwsgi environment variables
    env = {
        'UWSGI_ENABLE_THREADS': '1',
        'UWSGI_HONOUR_RANGE': '1',
    }
    if boolean_ish(os.environ.get('ENABLE_UWSGI_CHEAPER', 'on')):
        env.update({
            'UWSGI_CHEAPER': '1',
            'UWSGI_CHEAPER_ALGO': 'busyness',
            'UWSGI_CHEAPER_INITIAL': '1',
            'UWSGI_CHEAPER_BUSINESS_VERBOSE': '1',
            'UWSGI_CHEAPER_BUSINESS_BACKLOG_ALERT': '10',
            'UWSGI_CHEAPER_OVERLOAD': '30',
        })
    env.update(os.environ)
    return env


def execute(args, script=None):
    # TODO: is cleanup needed before calling exec? (open files, ...)
    command = script or args[0]
    os.execvpe(command, args, get_env())


def get_static_serving_args(base_url, root, header_patterns):
    base_path = str(furl.furl(base_url).path).lstrip('/')

    args = [
        f'--static-map=/{base_path}={root}',
        '--route={} addheader:Vary: Accept-Encoding'.format(
            os.path.join('^', base_path, '.*'),
        ),
    ]

    for pattern, headers in header_patterns:
        pattern = os.path.join('^', base_path, pattern)
        for k, v in headers.items():
            args.append(f'--route={pattern} addheader:{k}: {v}')
        args.append(f'--route={pattern} last:')

    return args


def start_uwsgi_command(settings, port=None):
    cmd = [
        'uwsgi',
        '--module=wsgi',
        '--http=0.0.0.0:{}'.format(port or settings.get('PORT')),
        '--master',
        '--workers={}'.format(settings['DJANGO_WEB_WORKERS']),
        '--max-requests={}'.format(settings['DJANGO_WEB_MAX_REQUESTS']),
        '--harakiri={}'.format(settings['DJANGO_WEB_TIMEOUT']),
        '--lazy-apps',
        '--need-app',
    ]

    serve_static = False

    if not settings['STATIC_URL_IS_ON_OTHER_DOMAIN']:
        serve_static = True
        cmd.extend(get_static_serving_args(
            settings['STATIC_URL'],
            settings['STATIC_ROOT'],
            settings['STATIC_HEADERS'],
        ))

    if not settings['MEDIA_URL_IS_ON_OTHER_DOMAIN']:
        serve_static = True
        cmd.extend(get_static_serving_args(
            settings['MEDIA_URL'],
            settings['MEDIA_ROOT'],
            settings['MEDIA_HEADERS'],
        ))

    if serve_static:
        cmd.extend([
            # Start 2 offloading threads for each worker
            '--offload-threads=2',

            # Cache resolved paths for up to 1 day (limited to 5k entries
            # of max 1kB size each)
            '--static-cache-paths=86400',
            '--static-cache-paths-name=staticpaths',
            '--cache2=name=staticpaths,items=5000,blocksize=1k,purge_lru,ignore_full',

            # Serve .gz files if that version is available
            '--static-gzip-all',
        ])

    return cmd
