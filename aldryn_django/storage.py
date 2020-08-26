import gzip
import os
import shutil

from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage, StaticFilesStorage,
)
from django.core.files.storage import FileSystemStorage
from django.utils.functional import lazy

import furl
from django_storage_url import dsn_configured_storage_class


# Required for backwards compatibility with django-filer
SCHEMES = {
    "default": "aldryn_django.storage.DefaultStorage",
    "s3": "aldryn_django.storage.S3MediaStorage",  # legacy check
}

DEFAULT_STORAGE_KEY = "DEFAULT_STORAGE_DSN"

DefaultStorage = dsn_configured_storage_class(DEFAULT_STORAGE_KEY)


def lazy_setting(name, func, type):
    def setter():
        value = func()
        setattr(settings, name, value)
        return value
    return lazy(setter, type)()


def get_default_storage_url():
    return DefaultStorage().base_url


def is_default_storage_on_other_domain():
    media_host = furl.furl(DefaultStorage().base_url).host
    return media_host not in settings.ALLOWED_HOSTS if media_host else False


class GZippedStaticFilesMixin(object):
    """
    Static files storage mixin to create a gzipped version of each static
    file, so that web servers (e.g. uWSGI) can take advantage of it and
    serve the optimized version.
    """
    gzip_ext = frozenset([
        '.html',
        '.css',
        '.js',
        '.json',
        '.svg',
        '.txt',
    ])

    def gzip_path(self, path):
        gz_path = path + '.gz'
        with self.open(path) as f_in:
            with self.open(gz_path, 'wb') as f_out:
                with gzip.GzipFile(fileobj=f_out) as gz_out:
                    shutil.copyfileobj(f_in, gz_out)
        return gz_path

    def iterfiles(self, path=''):
        dirs, files = self.listdir(path)
        for dir in dirs:
            for file in self.iterfiles(os.path.join(path, dir)):
                yield file
        for file in files:
            yield os.path.join(path, file)

    def post_process(self, paths, dry_run=False, **options):
        superclass = super(GZippedStaticFilesMixin, self)
        if hasattr(superclass, 'post_process'):
            post_processed = (
                superclass.post_process(paths, dry_run=dry_run, **options)
            )
        else:
            post_processed = []

        for processed in post_processed:
            yield processed

        if dry_run:
            return

        if not isinstance(self, FileSystemStorage):
            return

        for path in self.iterfiles():
            if os.path.splitext(path)[1] in self.gzip_ext:
                self.gzip_path(path)


class S3MediaStorage:
    pass


class GZippedStaticFilesStorage(GZippedStaticFilesMixin, StaticFilesStorage):
    pass


class ManifestGZippedStaticFilesStorage(GZippedStaticFilesMixin, ManifestStaticFilesStorage):
    pass
