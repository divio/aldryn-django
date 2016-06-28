import shutil
import mimetypes
import subprocess

from django.contrib.staticfiles.finders import get_finders
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


class Command(BaseCommand):
    help = 'Optimize static images prior to collectstatic'
    setting_names = [
        'STATIC_IMAGES_OPTIMIZE_COMMAND',
        'THUMBNAIL_OPTIMIZE_COMMAND',
    ]

    def get_settings(self):
        for setting_name in self.setting_names:
            try:
                return getattr(settings, setting_name)
            except AttributeError:
                pass
        else:
            return {}

    def handle(self, *args, **options):
        ignore_patterns = ['CVS', '.*', '*~']
        base_path = settings.BASE_DIR.rstrip('/') + '/'
        optimize_commands = self.get_settings()

        for finder in get_finders():
            for path, storage in finder.list(ignore_patterns):
                if not storage.path(path).startswith(base_path):
                    # Do not process images found in static dirs of third party
                    # apps.
                    continue
                mimetype = mimetypes.guess_type(path)[0]
                if not mimetype:
                    # Unknown mime type, ignore the file.
                    continue
                generic_type, image_type = mimetype.split('/', 1)
                if generic_type != 'image':
                    # Only process images.
                    continue
                if image_type in optimize_commands:
                    self.optimize(
                        storage,
                        path,
                        image_type,
                        optimize_commands[image_type],
                    )

    def optimize(self, storage, path, image_type, command):
        with NamedTemporaryFile() as temp_image:
            # Copy the image to the temporary file
            with storage.open(path, 'r+') as image:
                shutil.copyfileobj(image, temp_image)
            temp_image.flush()
            temp_image.seek(0)

            # Optimize the image
            optimize_command = command.format(filename=temp_image.name)
            self.stdout.write('>>> {}'.format(optimize_command))
            subprocess.check_call(optimize_command, shell=True)
            self.stdout.write('')

            # Save the image back from the temporary file into the storage
            with open(temp_image.name) as fh:
                storage.delete(path)
                storage.save(path, File(fh))
