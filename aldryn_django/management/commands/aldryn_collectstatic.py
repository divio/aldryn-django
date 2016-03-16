import os
import gzip
import shutil

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


def iterfiles(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


class Command(BaseCommand):
    help = 'Collect static files by following Aldryn conventions'
    gzip_ext = frozenset([
        '.html',
        '.css',
        '.js',
        '.json',
        '.svg',
        '.txt',
    ])

    def handle(self, *args, **options):
        # Defer static collection to Django
        call_command(
            'collectstatic',
            interactive=False,
            stdout=self.stdout,
        )

        # Gzip all files as appropriate
        for path_in in iterfiles(settings.STATIC_ROOT):
            if os.path.splitext(path_in)[1] in self.gzip_ext:
                path_out = path_in + '.gz'
                with open(path_in, 'rb') as f_in:
                    self.stdout.write('Compressing {}...'.format(path_in))
                    with gzip.open(path_out, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
