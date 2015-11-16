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
        'Django==1.8.6',

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
        'boto',
        'djeese-fs',

        # security related (insecure platform warnings)
        'cryptography',
        'ndg-httpsclient',
        'certifi',
        'pyOpenSSL',

        # TODO: should be in (aldryn-)django-cms
        'django-reversion',
        
        # TODO: aldryn-sites claims it doesn't support django>1.7
        # 'aldryn-sites',
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
