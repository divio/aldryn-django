#!/usr/bin/env python
from setuptools import find_packages, setup

from aldryn_django import __version__


REQUIREMENTS = [
    'aldryn-addons',
    'Django==4.0.9',

    # setup utils
    'dj-database-url',
    'dj-email-url',
    'dj-redis-url',
    'django-cache-url',
    'django-getenv',
    'aldryn-client',
    'furl',

    # error reporting
    'aiocontextvars',
    'sentry-sdk',

    # wsgi server related
    'uwsgi',

    # database
    'psycopg2',

    # storage
    'django-storage-url',
    'django-storages[boto3]',
    'django-storages[azure]',

    # helpers
    'click',
    'aldryn-sites>=0.5.6',
    'easy-thumbnails>=2.2',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 4.0',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
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
    license='BSD-3-Clause',
    description='An opinionated Django setup bundled as an Aldryn Addon',
    long_description=open('README.rst').read(),
    packages=find_packages(),
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
