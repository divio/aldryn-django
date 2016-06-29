CHANGELOG
=========

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
