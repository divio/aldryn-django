#-*- coding: utf-8 -*-
from django.conf import settings

from storages.backends import s3boto
import urlparse
import urllib


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
            # Setting an ACL requires us to grant the user the PutObjectAcl
            # permission as well, even if it matches the default bucket ACL.
            # XXX: Ideally we would thus set it to `None`, but due to how
            # easy_thumbnails works internally, that causes thumbnail
            # generation to fail...
            default_acl='public-read',
            querystring_auth=False,
        )


urlparse.uses_netloc.append('s3')
urlparse.uses_netloc.append('djfs')

SCHEMES = {
    's3': 'aldryn_django.storage.S3MediaStorage',
    'djfs': 'fs.django_storage.DjeeseFSStorage',
}


def parse_storage_url(url):
    config = {}
    url = urlparse.urlparse(url)

    scheme = url.scheme.split('+', 1)

    config['DEFAULT_FILE_STORAGE'] = SCHEMES[scheme[0]]

    if scheme[0] == 's3':
        config.update({
            'AWS_MEDIA_ACCESS_KEY_ID': urllib.unquote(url.username or ''),
            'AWS_MEDIA_SECRET_ACCESS_KEY': urllib.unquote(url.password or ''),
            # Ignore the .s3.amazonaws.com part
            'AWS_MEDIA_STORAGE_BUCKET_NAME': url.hostname.split('.', 1)[0],
            'AWS_MEDIA_BUCKET_PREFIX': url.path.lstrip('/'),
        })
    elif scheme[0] == 'djfs':
        hostname = ('{}:{}'.format(url.hostname, url.port)
                    if url.port else url.hostname)
        config.update({
            'DJEESE_STORAGE_ID': url.username or '',
            'DJEESE_STORAGE_KEY': url.password or '',
            'DJEESE_STORAGE_HOST': urlparse.urlunparse((
                scheme[1],
                hostname,
                url.path,
                url.params,
                url.query,
                url.fragment,
            )),
        })

    return config
