CHANGELOG
=========


1.11.10.1 (unreleased)
---------------------

* Update to Django 1.11.10
  see https://docs.djangoproject.com/en/1.11/releases/1.11.10/
  for details


1.11.9.1 (2018-01-19)
---------------------

* Update to Django 1.11.9


1.11.5.2 (2017-10-10)
---------------------

* Added new setting "session_timeout" to set SESSION_COOKIE_AGE.


1.11.5.1 (2017-09-06)
---------------------

* Upgrade Django to 1.11.5 (fixes CVE-2017-12794)
  see https://www.djangoproject.com/weblog/2017/sep/05/security-releases/
  for details


1.11.3.3 (2017-08-29)
---------------------

* Updated Django to 1.11.3 (previous versions of Aldryn Django 1.11.3.x were installing 1.11.1).


1.11.3.3 (2017-07-21)
---------------------

* Allow uwgsi flag 'honour range' to be environment variable configurable


1.11.3.2 (2017-07-10)
---------------------

* Configure Languages from environment variables
* Use django-storages instead of django-storages-redux
* Minor Bugfixes


1.11.3.1 (2017-07-10)
---------------------

* Upgrade Django to 1.11.3


1.11.1.1 (2017-05-18)
---------------------

* Upgrade Django to 1.11.1


1.11.0.2 (2017-04-23)
---------------------

* Upgrade Django to 1.11


1.10.7.1 (2017-04-05)
---------------------

* Upgrade Django to 1.10.7 (fixes CVE-2017-7233 and CVE-2017-7234)
  see https://www.djangoproject.com/weblog/2017/apr/04/security-releases/
  for details


1.10.6.3 (2017-03-29)
---------------------

* Fixed an issue with misleading setting name


1.10.6.2 (2017-03-29)
---------------------

* Added a new setting that allows users to disable the language prefix on urls
  for the default language.


1.10.6.1 (2017-03-21)
---------------------

* Upgrade Django to 1.10.6
* Fix DISABLE_S3_MEDIA_HEADERS_UPDATE env var parsing


1.10.5.0 (2017-02-28)
---------------------

* Upgrade Django to 1.10.5


1.9.11.2 (2016-11-19)
---------------------

* Enable Range request support in uWSGI


1.9.11.1 (2016-11-18)
---------------------

* Support setting SERVER_EMAIL and DEFAULT_FROM_EMAIL from env vars


1.9.11.0 (2016-11-01)
---------------------

* Upgrade Django to 1.9.11


1.9.10.1 (2016-10-27)
---------------------

* Get the S3 signature version from the DSN


1.9.10.0 (2016-09-26)
---------------------

* Upgrade Django to 1.9.10


1.9.8.2 (2016-08-10)
--------------------

* Use logging.NullHandler


1.9.8.1 (2016-08-05)
--------------------

* Do not redirect https requests to http when `SECURE_SSL_REDIRECT`
  is not explicitly set to `False`.
* Environment var for `X-Forwarded-Host` header support.
* Support for `EMAIL_URL` environment variable.


1.9.8.0 (2016-07-19)
--------------------

* Upgrade Django to 1.9.8


1.9.7.9 (2016-07-07)
--------------------

* fix gzip issue with python 3


1.9.7.8 (2016-07-05)
--------------------

* geodjango support


1.9.7.7 (2016-06-29)
--------------------

* hotfix


1.9.7.6 (2016-06-29)
--------------------

* add a middleware to allow disabling random comments for specific
  configured views


1.9.7.5 (2016-06-29)
--------------------

* fix a bug in the headers update command for old S3 storage buckets
* optimize performance for overall S3 headers update


1.9.7.4 (2016-06-28)
--------------------

* hotfix for the static images optimization command


1.9.7.3 (2016-06-28)
--------------------

* hotfix for the static images optimization command


1.9.7.2 (2016-06-28)
--------------------

* revert the changes introduced in 1.9.7.2 and provide a better help text
  for static file names hashing


1.9.7.1 (2016-06-27)
--------------------

* allow static files storage settings to be set for test/live independently


1.9.7.0 (2016-06-27)
--------------------

* upgrade to django 1.9.7


1.9.6.9 (2016-06-24)
--------------------

* support bucket names containing dots


1.9.6.8 (2016-06-23)
--------------------

* upgrade boto
* add an addon setting to enable manifest static files storage
* add utilities to optimize images


1.9.6.7 (2016-06-17)
--------------------

* support gzipping responses (including BREACH/CRIME prevention)
* support serving static files with an alternate domain


1.9.6.4 (2016-06-14)
--------------------

* add a management command to update the headers for existing media files stored
  on S3.
* re-renable lazy-apps
* optionally read the media domain from the storage DSN
* tune staticfiles serving from uwsgi
* use cached template loaders
* do not use nginx to add browser caching


1.9.6.3 (2016-06-13)
--------------------

* allow to set custom headers for file uploaded to S3 based on the MEDIA_HEADERS
  setting.
* pin django-reversion to < 2.0.0 as we don't officially support it yet.


1.9.6.2 (2016-06-10)
--------------------

* disable pagespeed for all admin pages


1.9.6.1 (2016-05-30)
--------------------

* redirect to admin on root url by default (to give first time site visitors a
  better experience)


1.9.6.0 (2016-05-10)
--------------------

* upgrade Django to 1.9.6
* initial stab at python3 compatibility


1.9.3.3 (2016-05-06)
--------------------

* correctly startup uwsgi with many command line options


1.9.3.2 (2016-03-03)
--------------------

* remove dependency to custom fork of django-tablib


1.9.3.1 (2016-03-02)
--------------------

* Django 1.9.3 (security release)
* uwsgi cheaper mode (prevents 502 at startup time)


1.9.2.1 (2016-02-15)
--------------------

* Django 1.9.2
* nginx/pagespeed settings updates


1.9.1.4 (2016-02-12)
--------------------

* bump tablib dependency


1.9.1.3 (2016-01-28)
--------------------

* first stable release
