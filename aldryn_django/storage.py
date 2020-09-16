import gzip
import os
import re
import shutil

from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage, StaticFilesStorage,
)
from django.core.files.storage import FileSystemStorage
from django.utils.functional import lazy
from django.utils.text import capfirst

import furl
from django_storage_url import dsn_configured_storage_class
from django_storage_url.backends import register_storage_class, s3


AWS_S3_ACL_PUBLIC_READ = {
    "Grantee": {
        "Type": "Group",
        "URI": "http://acs.amazonaws.com/groups/global/AllUsers",
    },
    "Permission": "READ",
}

# Required for backwards compatibility with django-filer
SCHEMES = {
    "default": "aldryn_django.storage.DefaultStorage",
    "s3": "aldryn_django.storage.S3MediaStorage",  #  legacy check
}

register_storage_class("s3", "aldryn_django.storage.S3MediaStorage")

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

    gzip_ext = frozenset([".html", ".css", ".js", ".json", ".svg", ".txt"])

    def gzip_path(self, path):
        gz_path = path + ".gz"
        with self.open(path) as f_in:
            with self.open(gz_path, "wb") as f_out:
                with gzip.GzipFile(fileobj=f_out) as gz_out:
                    shutil.copyfileobj(f_in, gz_out)
        return gz_path

    def iterfiles(self, path=""):
        dirs, files = self.listdir(path)
        for dir in dirs:
            for file in self.iterfiles(os.path.join(path, dir)):
                yield file
        for file in files:
            yield os.path.join(path, file)

    def post_process(self, paths, dry_run=False, **options):
        superclass = super(GZippedStaticFilesMixin, self)
        if hasattr(superclass, "post_process"):
            post_processed = superclass.post_process(paths, dry_run=dry_run, **options)
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


class S3MediaStorage(s3.S3Storage):
    ALLOWED_PARAMETERS = [
        "CacheControl",
        "ContentDisposition",
        "ContentEncoding",
        "ContentLanguage",
        "ContentType",
    ]

    def __init__(self, dsn):
        super().__init__(dsn)

        # MEDIA_HEADERS is a list of tuples containing a regular expression
        # to match against a path, and a dictionary of HTTP headers to be
        # returned with the resource identified by the path when it is
        # requested.
        # The headers are applied in the order they where declared, and
        # processing stops at the first match.
        # E.g.:
        #
        #    MEDIA_HEADERS = [
        #        (r'media/cache/.*', {
        #            'Cache-Control': 'max-age={}'.format(3600 * 24 * 365),
        #        })
        #    ]
        #
        media_headers = getattr(settings, "MEDIA_HEADERS", [])
        self.media_headers = [(re.compile(r), headers) for r, headers in media_headers]

    def _headers_for_path(self, path, headers):
        for pattern, headers_override in self.media_headers:
            if pattern.match(path) is not None:
                headers.update(headers_override)
                break
        return headers

    def _get_write_parameters(self, name, content=None):
        """
        Overwrite of the S3Storage function
        """
        params = super()._get_write_parameters(name, content)
        # Calling _prepare_headers in a separate call because params could have
        # more values than the allowed ones from `_prepare_headers`.
        new_headers = self._prepare_headers(name, {})
        params.update(new_headers)
        return params

    def _prepare_headers(self, path, headers):
        """
        Actually does the header update but only returns allowed headers which
        are not `None`.
        """
        tmp_headers = self._headers_for_path(path, headers)
        # Cleanup key format and only use valid headers
        new_headers = {}
        for k, v in tmp_headers.items():
            clean_key = "".join(map(capfirst, k.split("-")))
            if clean_key in self.ALLOWED_PARAMETERS:
                new_headers[clean_key] = v

        # Another cleanup to only use relevant data
        new_headers = {k: v for k, v in new_headers.items() if v is not None}

        return new_headers

    def update_headers(self):
        """
        Updates the headers for files in the s3 bucket according to the
        `MEDIA_HEADERS` setting.

        A header change is done, when the new headers differ from the existing
        headers of the file and the file has `public-read` access. Files with
        other perimissions like `private` will not be updated.
        """
        updated, total = 0, 0

        for object_summary in self.bucket.objects.filter(Prefix=self.location):
            total += 1

            obj = object_summary.Object()

            # Only change headers for files with a `public-read` access.
            if AWS_S3_ACL_PUBLIC_READ not in obj.Acl().grants:
                continue

            old_headers = {
                "CacheControl": obj.cache_control,
                "ContentDisposition": obj.content_disposition,
                "ContentEncoding": obj.content_encoding,
                "ContentLanguage": obj.content_language,
                "ContentType": obj.content_type,
            }
            old_headers = {k: v for k, v in old_headers.items() if v is not None}

            # Prepare new headers
            new_headers = self._prepare_headers(obj.key, old_headers.copy())
            if new_headers != old_headers:

                # Another cleanup to only use relevant data
                # Using `copy_from` to copy the file on itself updates the
                # headers
                obj.copy_from(
                    CopySource={"Bucket": obj.bucket_name, "Key": obj.key},
                    **new_headers,
                    MetadataDirective="REPLACE",
                    # This is valid because we check the permission to be
                    # `public-read` earlier
                    ACL="public-read"
                )
                updated += 1

        return updated, total


class GZippedStaticFilesStorage(GZippedStaticFilesMixin, StaticFilesStorage):
    pass


class ManifestGZippedStaticFilesStorage(
    GZippedStaticFilesMixin, ManifestStaticFilesStorage
):
    pass
