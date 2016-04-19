CHANGELOG
=========

1.6.11.25 (2016-04-19)
----------------------

* tune uwsgi static files serving:
   * set far-future expiration for hashed filenames
   * use offloading threads to serve static files
   * cache resolved static file paths for even better performance
   * serve gzipped versions when available
* optionally read the media domain from the storage DSN
* add an aldryn_collectstatic command which also gzip-compresses static files
* enable cached template loader (can be explicitly disabled by setting the
  ``DISABLE_TEMPLATE_CACHE`` env variable to true)
* serve static files using uwsgi --static-map (is automatically disabled when
  syncing is enabled using ``ENABLE_SYNCING``)
* switch to ManifestStaticFilesStorage for ``STATICFILES_STORAGE``
* remove dependency to custom fork of django-tablib


1.6.11.22 (2016-02-25)
----------------------

* switch to more reliable (no 502s) uwsgi startup mode (uwsgi cheaper)

1.6.11.21 (2016-02-17)
----------------------

* install django-tablib so 1.6.x behaves the same as aldryn-django 1.8.x and 1.9.x

1.6.11.20 (2016-01-21)
----------------------

* use fixed internal version of boto (upstream merge/release pending)


1.6.11.19 (2016-01-14)
----------------------

* restrict to compatible django_compressor version


1.6.11.18 (2016-01-11)
----------------------

* adds django-secure


0.1 (2015-08-27)
----------------

Initial release
