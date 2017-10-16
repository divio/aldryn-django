CHANGELOG
=========

1.8.18.5 (2017-10-10)
---------------------

* Added new setting "session_timeout" to set SESSION_COOKIE_AGE.


1.8.18.4 (2017-07-07)
---------------------

* Configure Languages from environment variables
* Use django-storages instead of django-storages-redux
* Minor Bugfixes


1.8.18.3 (2017-05-25)
---------------------

* Mark language names as translatable


1.8.18.2 (2017-05-16)
---------------------

* Allow users to configure aldryn sites redirect type via env variable


1.8.18.1 (2017-04-05)
---------------------

* Upgrade Django to 1.8.18 (fixes CVE-2017-7233 and CVE-2017-7234)
  see https://www.djangoproject.com/weblog/2017/apr/04/security-releases/
  for details


1.8.17.3 (2017-03-29)
---------------------

* Fixed an issue with misleading setting name


1.8.17.2 (2017-03-29)
---------------------

* Added a new setting that allows users to disable the language prefix on urls
  for the default language.


1.8.17.1 (2017-03-21)
---------------------

* Upgrade Django to 1.8.17
* Remove pinned dependency to internal easy-thumbnails release


1.8.16.3 (2016-11-19)
---------------------

* Enable Range request support in uWSGI


1.8.16.2 (2016-11-17)
---------------------

* Support setting SERVER_EMAIL and DEFAULT_FROM_EMAIL from env vars


1.8.16.1 (2016-11-11)
---------------------

* Get the S3 signature version from the DSN


1.8.16.0 (2016-11-01)
---------------------

* Upgrade Django to 1.8.16


1.8.15.0 (2016-09-26)
---------------------

* Upgrade Django to 1.8.15


1.8.14.2 (2016-08-05)
---------------------

* Do not redirect https requests to http when `SECURE_SSL_REDIRECT`
  is not explicitly set to `False`.


1.8.14.1 (2016-07-26)
---------------------

* env var for X-Forwarded-Host header support
* support for EMAIL_URL environment variable


1.8.14.0 (2016-07-19)
---------------------

* Upgrade Django to 1.8.14


1.8.13.8 (2016-07-07)
---------------------

* fix gzip issue with python 3


1.8.13.7 (2016-07-05)
---------------------

* geodjango support


1.8.13.6 (2016-06-29)
---------------------

* hotfix


1.8.13.5 (2016-06-29)
---------------------

* add a middleware to allow disabling random comments for specific
  configured views


1.8.13.4 (2016-06-29)
---------------------

* fix a bug in the headers update command for old S3 storage buckets
* optimize performance for overall S3 headers update


1.8.13.3 (2016-06-28)
---------------------

* hotfix for static images optimization


1.8.13.2 (2016-06-28)
---------------------

* hotfix for static images optimization


1.8.13.1 (2016-06-28)
---------------------

* revert the changes introduced in 1.8.11.8 and provide a better help text
  for static file names hashing


1.8.13.0 (2016-06-27)
---------------------

* upgrade django to 1.8.13


1.8.11.8 (2016-06-27)
---------------------

* allow static files storage settings to be set for test/live independently


1.8.11.7 (2016-06-24)
---------------------

* support bucket names containing dots


1.8.11.6 (2016-06-23)
---------------------

* upgrade boto
* add an addon setting to enable manifest static files storage
* add utilities to optimize images
* support gzipping responses (including BREACH/CRIME prevention)
* support serving static files with an alternate domain
* optionally read the media domain from the storage DSN


1.8.11.5 (2016-06-14)
---------------------

* bugfix release


1.8.11.4 (2016-06-14)
---------------------

* do not use nginx for caching and support declarative headers for both media and
  static files serving.


1.8.11.3 (2016-06-13)
---------------------

* allow to set custom headers for file uploaded to S3 based on the MEDIA_HEADERS
  setting (along with a management command to update existing objects).


1.8.11.2 (2016-06-10)
---------------------

* disable pagespeed for all admin pages


1.8.11.1 (2016-05-30)
---------------------

* redirect to admin on root url by default (to give first time site visitors a
  better experience)
* bump to django 1.8.11


1.8.10.7 (2016-05-06)
---------------------

* correctly startup uwsgi with many command line options


1.8.10.6 (2016-03-17)
---------------------

* re-enable ``--lazy-apps`` loading across the board


1.8.10.5 (2016-03-16)
---------------------

* bugfix release


1.8.10.4 (2016-03-16)
---------------------

* remove ManifestStaticFilesStorage setting (this setting can easily be
  overridden in the project settings file)
* tune uwsgi static files serving:
   * set far-future expiration for hashed filenames
   * use offloading threads to serve static files
   * cache resolved static file paths for even better performance
   * serve gzipped versions when available
* optionally read the media domain from the storage DSN
* add an aldryn_collectstatic command which also gzip-compresses static files


1.8.10.3 (2016-03-15)
---------------------

* enable cached template loader (can be explicitly disabled by setting the
  ``DISABLE_TEMPLATE_CACHE`` env variable to true)
* serve static files using uwsgi --static-map (is automatically disabled when
  syncing is enabled using ``ENABLE_SYNCING``)
* switch to ManifestStaticFilesStorage for ``STATICFILES_STORAGE``


1.8.10.2 (2016-03-03)
---------------------

* remove dependency to custom fork of django-tablib


1.8.10.1 (2016-03-02)
---------------------

* Django 1.8.10 (security release)


1.8.9.5 (2016-02-25)
--------------------

* switch to more reliable (no 502s) uwsgi startup mode (uwsgi cheaper)


1.8.9.4 (2016-02-15)
--------------------

* use newer release of django-tablib


1.8.9.3 (2016-02-10)
--------------------

* fix incorrect pinned boto version
* Django 1.8.9
* fix pagespeed setup
* use SITE_NAME environment variable for auto-configuration with aldryn-sites


1.8.8.2 (2016-01-11)
--------------------

* use native Django 1.8 alternative to django-secure


1.8.8.1 (2016-01-11)
--------------------

* adds django-secure
* adds aldryn-sites


1.8.6.0 (2015-11-17)
--------------------

* Initial release
