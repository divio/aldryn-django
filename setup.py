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
    dependency_links=(
        "https://control-panel-live-extra-packages.s3.amazonaws.com/django-formtools/django-formtools-1.0.0.1.tar.gz#egg=django-formtools",
    ),
    install_requires=(
        'aldryn-addons',
        # security backport of Django from
        # https://devpi.divio.ch/divio/django-backports/+simple/Django/
        'Django==1.6.11.post5',

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

        # security
        'django-secure',

        # other setup helpers
        'aldryn-sites',

        # not strictly needed by Django, but aldryn-django-cms needs it and it
        # must be <1.9 for Django 1.6.x support
        'django-reversion<1.9',

        # not strictly needed by Django, but aldryn-django-cms installs it and
        # the official version 1.0.0 on pypi requires Django>=1.7
        'django-formtools==1.0.0.1',

        # TODO: Remove after django-tablib would be released
        # use internal package with django 1.8+ support instead of outdated
        # needed for aldryn-events and aldryn-forms export features.
        'django-tablib==3.1.1.2',

        # Force a Django 1.6 compatible version.
        'django-simple-captcha<0.4.8',
        'django-mptt<0.8.0',
        'django-treebeard==3.0',  # required by django-cms
        'django_compressor<2.0',  # required by aldryn-django-cms
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
