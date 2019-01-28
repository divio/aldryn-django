import os

from six.moves.urllib import parse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import yurl

from boto.s3.connection import (
    SubdomainCallingFormat,
    OrdinaryCallingFormat,
)

from storages.backends import s3boto


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
