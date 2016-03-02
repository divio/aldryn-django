# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_django import __version__

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
        'Django==1.9.3',

        # setup utils
        'dj-database-url',
        'dj-email-url',
        'dj-redis-url',
        'django-cache-url',
        'django-appconf',
        'django-getenv',
        'aldryn-client',
        'webservices',
        'pyaml',
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
        'subprocess32',

        # storage
        'django-storages-redux',
        # boto==2.38.0.1 is an internal release that contains
        # https://github.com/stefanfoulis/boto/tree/2.38.0.1
        # a fix for boto falsly adding authentication parameters to s3 url even
        # though configured not to.
        'boto==2.38.0.1',
        'djeese-fs',

        # security: avoid python insecure platform warnings
        'cryptography',
        'ndg-httpsclient',
        'certifi',
        'pyOpenSSL',

        # helpers
        'aldryn-sites>=0.5.2',

        # TODO: should be in (aldryn-)django-cms
        # However, it doesn't know which version of Django is being installed,
        # so it stays here.
        'django-reversion>=1.10.0',
        'django-treebeard>=4.0',

        # TODO: Remove after django-tablib would be released
        # use internal package with django 1.8 support instead of outdated
        # needed for aldryn-events and aldryn-forms export features.
        'django-tablib==3.1.1.2',
        'easy-thumbnails==2.2.1.1',
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
