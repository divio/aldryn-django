CHANGELOG
=========

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
