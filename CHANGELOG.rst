CHANGELOG
=========

1.8.10.4 (2016-03-16)
---------------------

* remove ManifestStaticFilesStorage setting (this setting can easily be
  overridden in the project settings file)
* tune uwsgi static files serving:
   * set far-future expiration for hashed filenames
   * use offloading threads to serve static files
   * cache resolved static file paths for even better performance
   * serve gzipped versions when available
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
