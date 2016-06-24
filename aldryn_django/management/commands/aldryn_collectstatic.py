import os
import gzip
import shutil
import warnings

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

from aldryn_django.storage import GZippedStaticFilesMixin


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
        warnings.warn((
            'aldryn_collectstatic is deprecated, please use a staticfiles\n'
            'storage backend supporting file gzipping, such as\n'
            'aldryn_django.storage.GZippedStaticFilesStorage, and just call\n'
            'the collectstatic management command instead.'
        ), DeprecationWarning)

        # Defer static collection to Django
        call_command(
            'collectstatic',
            interactive=False,
            stdout=self.stdout,
        )

        if isinstance(staticfiles_storage, GZippedStaticFilesMixin):
            # No need to run gzipping twice if the currently configured storage
            # backend already does it
            return

        # Gzip all files as appropriate
        for path_in in iterfiles(settings.STATIC_ROOT):
            if os.path.splitext(path_in)[1] in self.gzip_ext:
                path_out = path_in + '.gz'
                with open(path_in, 'rb') as f_in:
                    self.stdout.write('Compressing {}...'.format(path_in))
                    with gzip.open(path_out, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
