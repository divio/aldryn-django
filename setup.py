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
        'Django==1.6.11.post3',

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

        # not strictly needed by Django, but aldryn-django-cms needs it and it
        # must be <1.9 for Django 1.6.x support
        'django-reversion<1.9',

        # not strictly needed by Django, but aldryn-django-cms installs it and
        # the official version 1.0.0 on pypi requires Django>=1.7
        'django-formtools==1.0.0.1',
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
