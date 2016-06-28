# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from aldryn_django import __version__


if sys.version_info[0] == 2:
    # on python2 the backport of subprocess32 is needed
    extra_dependencies = (
        'subprocess32',
    )
else:
    extra_dependencies = ()


setup(
    name="aldryn-django",
    version=__version__,
    description='An opinionated Django setup bundled as an Aldryn Addon',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-django',
    packages=find_packages(),
    install_requires=(
        'aldryn-addons',
        'Django==1.8.13',

        # setup utils
        'dj-database-url',
        'dj-email-url',
        'dj-redis-url',
        'django-cache-url',
        'django-appconf',
        'django-getenv',
        'aldryn-client',
        'webservices',
        'yurl',

        # error reporting
        'raven',
        'opbeat',

        # wsgi server related
        'uwsgi',
        'dj-static',

        # database
        'psycopg2',
        'structlog',
        'click',

        # storage
        'django-storages-redux',
        'boto>=2.40.0',
        'djeese-fs',

        # security: avoid python insecure platform warnings
        'cryptography',
        'ndg-httpsclient',
        'certifi',
        'pyOpenSSL',
        # required until https://code.djangoproject.com/ticket/20869 lands
        'django-debreach',

        # helpers
        'aldryn-sites>=0.5.2',

        # TODO: should be in (aldryn-)django-cms
        'django-reversion<1.9',

        'easy-thumbnails==2.2.1.1',
    ) + extra_dependencies,
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
