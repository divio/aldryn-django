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
        'Django==1.6.11',

        # setup utils
        'dj-database-url',
        'dj-email-url',
        'dj-redis-url',
        'django-cache-url',
        'django-appconf',
        'django-dotenv',
        'django-getenv',
        'aldryn-client',
        'webservices',

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
        'South',

        # storage
        'django-storages',
        'boto',
        'djeese-fs',

        # securty related (insecure platform warnings)
        'cryptography',
        'ndg-httpsclient',
        'certifi',
        'pyOpenSSL',

        # other setup helpers
        'aldryn-sites',

        # not strictly needed by Django, but aldryn-cms needs it and it must
        # be <1.9 for Django 1.6.x support
        'django-reversion<1.9',
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
