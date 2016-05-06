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
        # security backport of Django from
        # https://devpi.divio.ch/divio/django-backports/+simple/Django/
        'Django==1.5.12',

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
        'subprocess32',
        'South',

        # storage
        'django-storages',
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

        # security
        'django-secure',

        # helpers
        'aldryn-sites>=0.5.1',

        # not strictly needed by Django, but aldryn-cms needs it and it must
        # be >1.7.0 (which is only for django 1.5.0)
        # that gives us only 1.7.1 for Django 1.5+ support, but to be safe if
        # critical issues would be fixed (which is none atm) specifying a range.
        'django-reversion>=1.7.1,<1.8',

        'django_compressor<2.0',  # required by aldryn-django-cms
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
