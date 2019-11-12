=========
Changelog
=========


1.11.26.2 (2019-11-12)
======================

* Added the ``--need-app`` command line flag to the uwsgi startup options


1.11.26.1 (2019-11-04)
======================

* Add Django 1.11.26 support


1.11.25.1 (2019-10-08)
======================

* Add Django 1.11.25 support


1.11.24.1 (2019-09-24)
======================

* Add Django 1.11.24 support


1.11.23.1 (2019-08-05)
======================

* Upgrade Django to 1.11.23
  (fixes CVE-2019-14232, CVE-2019-14233, CVE-2019-14234, CVE-2019-14235)
  see https://www.djangoproject.com/weblog/2019/aug/01/security-releases/
  for details


1.11.22.4 (2019-07-29)
======================

* Serve static files from ``django.conf.urls.static`` during local development


1.11.22.3 (2019-07-24)
======================

* Removed ``ENABLE_SYNCING`` and thus serving files always from uwsgi
* Removed dj-static requirement and relevant code


1.11.22.2 (2019-07-16)
======================

* Removed faulty help text for languages settings


1.11.22.1 (2019-07-01)
======================

* Upgrade Django to 1.11.22 (fixes CVE-2019-12781)
  see https://www.djangoproject.com/weblog/2019/jul/01/security-releases/
  for details


1.11.21.1 (2019-06-03)
======================

* Upgrade Django to 1.11.21 (fixes CVE-2019-12308)
  see https://www.djangoproject.com/weblog/2019/jun/03/security-releases/
  for details


1.11.20.4 (2019-04-15)
======================

* Pinned django-mptt due to compatibility issues with Python 2


1.11.20.3 (2019-04-10)
======================

* Pinned django-select due to compatibility issues with Django 1.11


1.11.20.2 (2019-04-09)
======================

* Replaced raven with sentry-sdk


1.11.20.1 (2019-02-11)
======================

* Upgrade Django to 1.11.20 (fixes CVE-2019-6975)
  see https://www.djangoproject.com/weblog/2019/feb/11/security-releases/
  for details
* Django 1.11.19 was faulty and is not provided on Divio Cloud, see
  https://code.djangoproject.com/ticket/30175 for details


1.11.18.3 (2019-01-29)
======================

* Added missing ``entry_points`` to ``setup.py``


1.11.18.2 (2019-01-29)
======================

* Added test matrix
* Adapted code base to align with other supported addons
* Allow users to configure aldryn sites redirect type via env variable


1.11.18.1 (2019-01-07)
======================

* Upgrade Django to 1.11.18 (fixes CVE-2019-3498)
  see https://www.djangoproject.com/weblog/2019/jan/04/security-releases/
  for details


1.11.17.1 (2018-12-17)
======================

* Add Django 1.11.17 support


1.11.15.1 (2018-08-01)
======================

* Upgrade Django to 1.11.15 (fixes CVE-2018-14574)


1.11.11.1 (2018-03-07)
======================

* Upgrade Django to 1.11.11 (fixes CVE-2018-7536 and CVE-2018-7537)
  see https://www.djangoproject.com/weblog/2018/mar/06/security-releases/
  for details
* Remove unsupported and deprecated Nginx/Pagespeed settings.
* Send release and environment tracking info along with Sentry events.
* Remove unused dependencies.


1.11.10.1 (2018-02-02)
======================

* Update to Django 1.11.10
  see https://docs.djangoproject.com/en/1.11/releases/1.11.10/
  for details.


1.11.9.1 (2018-01-19)
=====================

* Update to Django 1.11.9.


1.11.5.2 (2017-10-10)
=====================

* Added new setting "session_timeout" to set SESSION_COOKIE_AGE.


1.11.5.1 (2017-09-06)
=====================

* Upgrade Django to 1.11.5 (fixes CVE-2017-12794)
  see https://www.djangoproject.com/weblog/2017/sep/05/security-releases/
  for details.


1.11.3.3 (2017-08-29)
=====================

* Updated Django to 1.11.3 (previous versions of aldryn-django 1.11.3.x were installing 1.11.1).


1.11.3.3 (2017-07-21)
=====================

* Allow uwgsi flag 'honour range' to be environment variable configurable.


1.11.3.2 (2017-07-10)
=====================

* Configure Languages from environment variables.
* Use django-storages instead of django-storages-redux.
* Minor Bugfixes.


1.11.3.1 (2017-07-10)
=====================

* Upgrade Django to 1.11.3.


1.11.1.1 (2017-05-18)
=====================

* Upgrade Django to 1.11.1.


1.11.0.2 (2017-04-23)
=====================

* Upgrade Django to 1.11.
