#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import find_packages, setup

from aldryn_django import __version__


if sys.version_info[0] == 2:
    # on python2 the backport of subprocess32 is needed
    extra_dependencies = [
        'subprocess32',
    ]
else:
    extra_dependencies = []


REQUIREMENTS = [
    'aldryn-addons',
    'Django==2.1.13',

    # setup utils
    'dj-database-url',
    'dj-email-url',
    'dj-redis-url',
    'django-cache-url',
    'django-getenv',
    'aldryn-client',
    'yurl',

    # error reporting
    'sentry-sdk',

    # wsgi server related
    'uwsgi',

    # database
    'psycopg2',

    # storage
    'django-storages',
    'boto>=2.40.0',
    'djeese-fs',

    # helpers
    'click',
    'aldryn-sites>=0.5.6',

    'easy-thumbnails>=2.2.1.1',
] + extra_dependencies


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 2.1',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='aldryn-django',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/divio/aldryn-django',
    license='BSD',
    description='An opinionated Django setup bundled as an Aldryn Addon',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
)
