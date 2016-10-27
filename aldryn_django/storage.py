import os
import re
import shutil
import gzip

from django.conf import settings
from django.contrib.staticfiles.storage import (
    StaticFilesStorage,
    ManifestStaticFilesStorage,
)
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured

from boto.s3.connection import (
    SubdomainCallingFormat,
    OrdinaryCallingFormat,
)

from six.moves.urllib import parse
from storages.backends import s3boto
import yurl


SCHEMES = {
    's3': 'aldryn_django.storage.S3MediaStorage',
    'djfs': 'fs.django_storage.DjeeseFSStorage',
}

parse.uses_netloc.append('s3')
parse.uses_netloc.append('djfs')


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


def parse_storage_url(url):
    config = {}
    url = parse.urlparse(url)

    scheme = url.scheme.split('+', 1)

    config['DEFAULT_FILE_STORAGE'] = SCHEMES[scheme[0]]

    if scheme[0] == 's3':
        query = parse.parse_qs(url.query)
        media_domain = query.get('domain', [None])[0]
        signature_ver = query.get('auth', ['s3v4'])[0]
        endpoint = url.hostname.rsplit('.', 3)
        bucket_name = endpoint[0]
        storage_host = '.'.join(endpoint[1:])

        if signature_ver == 's3v4':
            os.environ['S3_USE_SIGV4'] = 'True'
        elif signature_ver == 's3':
            os.environ['S3_USE_SIGV4'] = ''
        else:
            raise ImproperlyConfigured('Unknown signature version: {}'
                                       .format(signature_ver))

        config.update({
            'AWS_MEDIA_ACCESS_KEY_ID': parse.unquote(url.username or ''),
            'AWS_MEDIA_SECRET_ACCESS_KEY': parse.unquote(url.password or ''),
            'AWS_MEDIA_STORAGE_BUCKET_NAME': bucket_name,
            'AWS_MEDIA_STORAGE_HOST': storage_host,
            'AWS_MEDIA_BUCKET_PREFIX': url.path.lstrip('/'),
            'AWS_MEDIA_DOMAIN': media_domain,
        })

        if not media_domain:
            media_domain = '.'.join([
                config['AWS_MEDIA_STORAGE_BUCKET_NAME'],
                config['AWS_MEDIA_STORAGE_HOST'],
            ])
        media_url = yurl.URL(
            scheme='https',
            host=media_domain,
            path=config['AWS_MEDIA_BUCKET_PREFIX'],
        )
        config['MEDIA_URL'] = media_url.as_string()
    elif scheme[0] == 'djfs':
        hostname = ('{}:{}'.format(url.hostname, url.port)
                    if url.port else url.hostname)
        config.update({
            'DJEESE_STORAGE_ID': url.username or '',
            'DJEESE_STORAGE_KEY': url.password or '',
            'DJEESE_STORAGE_HOST': parse.urlunparse((
                scheme[1],
                hostname,
                url.path,
                url.params,
                url.query,
                url.fragment,
            )),
        })
        media_url = yurl.URL(
            scheme=scheme[1],
            host=url.hostname,
            path=url.path,
            port=url.port or '',
        )
        config['MEDIA_URL'] = media_url.as_string()
    if config['MEDIA_URL'] and not config['MEDIA_URL'].endswith('/'):
        # Django (or something else?) silently sets MEDIA_URL to an empty
        # string if it does not end with a '/'
        config['MEDIA_URL'] = '{}/'.format(config['MEDIA_URL'])
    return config


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


class GZippedStaticFilesStorage(GZippedStaticFilesMixin,
                                StaticFilesStorage):
    pass


class ManifestGZippedStaticFilesStorage(GZippedStaticFilesMixin,
                                        ManifestStaticFilesStorage):
    pass
