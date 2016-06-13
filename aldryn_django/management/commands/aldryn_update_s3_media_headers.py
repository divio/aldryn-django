from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure all headers for S3 uploaded files are up to date'

    def handle(self, *args, **options):
        if not hasattr(default_storage, 'update_headers'):
            self.stdout('The default media files storage does not '
                        'support updating headers')
        all_files, updated = default_storage.update_headers()
        self.stdout('{}/{} files updated'.format(updated, all_files))
