from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Ensure all headers for S3 uploaded files are up to date'

    def handle(self, *args, **options):
        if not hasattr(default_storage, 'update_headers'):
            raise CommandError('The default media files storage does not '
                               'support updating headers')
        updated, total = default_storage.update_headers()
        self.stdout.write('{}/{} files updated'.format(updated, total))
