import os
import re

from django.conf import settings

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
        # We cannot use a function call or a partial here. Instead, we have to
        # create a subclass because django tries to recreate a new object by
        # calling the __init__ of the returned object (with no arguments).
        super(S3MediaStorage, self).__init__(
            access_key=settings.AWS_MEDIA_ACCESS_KEY_ID,
            secret_key=settings.AWS_MEDIA_SECRET_ACCESS_KEY,
            bucket_name=settings.AWS_MEDIA_STORAGE_BUCKET_NAME,
            location=settings.AWS_MEDIA_BUCKET_PREFIX,
            host=settings.AWS_MEDIA_STORAGE_HOST,
            custom_domain=settings.AWS_MEDIA_DOMAIN,
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
                key.copy(self.bucket.name, key,
                         metadata=new_headers, preserve_acl=True)
                updated += 1

        return updated, total


def parse_storage_url(url):
    config = {}
    url = parse.urlparse(url)

    scheme = url.scheme.split('+', 1)

    config['DEFAULT_FILE_STORAGE'] = SCHEMES[scheme[0]]

    if scheme[0] == 's3':
        os.environ['S3_USE_SIGV4'] = 'True'

        media_domain = parse.parse_qs(url.query).get('domain', [None])[0]

        config.update({
            'AWS_MEDIA_ACCESS_KEY_ID': parse.unquote(url.username or ''),
            'AWS_MEDIA_SECRET_ACCESS_KEY': parse.unquote(url.password or ''),
            'AWS_MEDIA_STORAGE_BUCKET_NAME': url.hostname.split('.', 1)[0],
            'AWS_MEDIA_STORAGE_HOST': url.hostname.split('.', 1)[1],
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
