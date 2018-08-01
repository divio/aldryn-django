import re

from django.conf import settings

from boto.s3.connection import (
    SubdomainCallingFormat,
    OrdinaryCallingFormat,
)

from storages.backends import s3boto


class S3MediaStorage(s3boto.S3BotoStorage):
    def __init__(self):
        bucket_name = settings.AWS_MEDIA_STORAGE_BUCKET_NAME

        if '.' in bucket_name:
            calling_format = OrdinaryCallingFormat()
        else:
            calling_format = SubdomainCallingFormat()

        # We cannot use a function call or a partial here. Instead, we have to
        # create a subclass because django tries to recreate a new object by
        # calling the __init__ of the returned object (with no arguments).
        super(S3MediaStorage, self).__init__(
            access_key=settings.AWS_MEDIA_ACCESS_KEY_ID,
            secret_key=settings.AWS_MEDIA_SECRET_ACCESS_KEY,
            bucket_name=bucket_name,
            location=settings.AWS_MEDIA_BUCKET_PREFIX,
            host=settings.AWS_MEDIA_STORAGE_HOST,
            custom_domain=settings.AWS_MEDIA_DOMAIN,
            calling_format=calling_format,
            # Setting an ACL requires us to grant the user the PutObjectAcl
            # permission as well, even if it matches the default bucket ACL.
            # XXX: Ideally we would thus set it to `None`, but due to how
            # easy_thumbnails works internally, that causes thumbnail
            # generation to fail...
            default_acl='public-read',
            querystring_auth=False,
        )
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
        media_headers = getattr(settings, 'MEDIA_HEADERS', [])
        self.media_headers = [
            (re.compile(r), headers) for r, headers in media_headers
        ]

    def _headers_for_path(self, path, headers):
        for pattern, headers_override in self.media_headers:
            if pattern.match(path) is not None:
                headers.update(headers_override)
                break
        return headers

    def _save_content(self, key, content, headers):
        headers = self._headers_for_path(self._key_path(key), headers)
        return super(S3MediaStorage, self)._save_content(key, content, headers)

    def _key_path(self, key):
        return self._decode_name(key.key)[len(self.location):].lstrip('/')

    def update_headers(self):
        updated, total = 0, 0

        dirlist = self.bucket.list(self._encode_name(self.location))
        for key in dirlist:
            path = self._key_path(key)
            key = self.bucket.get_key(key.name)

            old_headers = {
                k.lower(): v
                for k, v in key._get_remote_metadata().items()
            }

            new_headers = self.headers.copy()
            if 'content-type' in old_headers:
                new_headers['content-type'] = old_headers['content-type']
            new_headers = self._headers_for_path(path, new_headers)
            new_headers = {k.lower(): v for k, v in new_headers.items()}

            total += 1

            if new_headers != old_headers:
                key.copy(
                    self.bucket.name, key,
                    metadata=new_headers,
                    preserve_acl=True,
                    validate_dst_bucket=False,
                )
                updated += 1

        return updated, total