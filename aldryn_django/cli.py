#-*- coding: utf-8 -*-
from __future__ import absolute_import
import click
import os
import sys
import yaml
from django.template import loader, Context
from django.conf import settings as django_settings
from aldryn_addons.utils import openfile, boolean_ish, senv


# add the current directory to pythonpath. So the project files can be read.
BASE_DIR = os.getcwd()
sys.path.insert(0, BASE_DIR)


@click.command()
@click.pass_obj
def web(ctx_obj):
    """
    launch the webserver of choice (uwsgi)
    """
    if any(boolean_ish(ctx_obj['settings'][key]) for key in ['ENABLE_NGINX', 'ENABLE_PAGESPEED', 'ENABLE_BROWSERCACHE']):
        # uwsgi behind nginx. possibly with pagespeed/browsercache
        start_with_nginx(ctx_obj['settings'])
    else:
        # pure uwsgi
        execute(start_uwsgi_command(settings=ctx_obj['settings'], port=80))


@click.command()
@click.pass_obj
def worker(ctx_obj):
    """
    coming soon: launch the background worker
    """
    # TODO: celery worker startup, once available
    pass


@click.command()
@click.pass_obj
def migrate(ctx_obj):
    """
    run any migrations needed at deploy time. most notably database migrations.
    """
    cmds = ctx_obj['settings']['MIGRATION_COMMANDS']
    click.echo('aldryn-django: running migration commands')
    for cmd in cmds:
        click.echo('    ----> {}'.format(cmd))
        exitcode = os.system(cmd)
        if exitcode != 0:
            sys.exit(exitcode)


@click.group()
@click.pass_context
def main(ctx):
    if not os.path.exists(os.path.join(BASE_DIR, 'manage.py')):
        raise click.UsageError('make sure you are in the same directory as manage.py')
    from . import startup
    startup._setup(BASE_DIR)
    ctx.obj = {
        'settings': {key: getattr(django_settings, key) for key in dir(django_settings)}
    }


main.add_command(web)
main.add_command(worker)
main.add_command(migrate)


def execute(args, script=None):
    # TODO: is cleanup needed before calling exec? (open files, ...)
    command = script or args[0]
    os.execvp(command, args)


def start_uwsgi_command(settings, port=None):
    return [
        'uwsgi',
        '--module=wsgi',
        '--http=0.0.0.0:{}'.format(port or settings.get('PORT')),
        '--workers={}'.format(settings['DJANGO_WEB_WORKERS']),
        '--max-requests={}'.format(settings['DJANGO_WEB_MAX_REQUESTS']),
        '--harakiri={}'.format(settings['DJANGO_WEB_TIMEOUT']),
        # '--honour-stdin',
    ]


def start_procfile_command(procfile_path):
    return [
        'forego',
        'start',
        '-f',
        procfile_path
    ]


def start_with_nginx(settings):
    # TODO: test with pagespeed and static or media on other domain
    if not all([settings['NGINX_CONF_PATH'], settings['NGINX_PROCFILE_PATH']]):
        raise click.UsageError('NGINX_CONF_PATH and NGINX_PROCFILE_PATH must be configured')
    procfile = yaml.safe_dump(
        {
            'nginx': 'nginx',
            'django': ' '.join(start_uwsgi_command(settings, port=settings['BACKEND_PORT']))
        },
        default_flow_style=False,
    )
    nginx_template = loader.get_template('aldryn_django/configuration/nginx.conf')
    context = Context(dict(settings))
    nginx_conf = nginx_template.render(context)
    with openfile(settings['NGINX_CONF_PATH']) as f:
        f.write(nginx_conf)
    with openfile(settings['NGINX_PROCFILE_PATH']) as f:
        f.write(procfile)
    execute(start_procfile_command(settings['NGINX_PROCFILE_PATH']))


