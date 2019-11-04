=========
Changelog
=========


2.1.14.1 (2019-11-04)
=====================

* Add Django 2.1.14 support


2.1.13.1 (2019-10-08)
=====================

* Add Django 2.1.13 support


2.1.12.1 (2019-09-24)
=====================

* Add Django 2.1.12 support


2.1.11.1 (2019-08-05)
=====================

* Upgrade Django to 2.1.11
  (fixes CVE-2019-14232, CVE-2019-14233, CVE-2019-14234, CVE-2019-14235)
  see https://www.djangoproject.com/weblog/2019/aug/01/security-releases/
  for details


2.1.10.4 (2019-07-29)
=====================

* Serve static files from ``django.conf.urls.static`` during local development


2.1.10.3 (2019-07-24)
=====================

* Removed ``ENABLE_SYNCING`` and thus serving files always from uwsgi
* Removed dj-static requirement and relevant code


2.1.10.2 (2019-07-16)
=====================

 * Removed faulty help text for languages settings


2.1.10.1 (2019-07-01)
=====================

* Upgrade Django to 2.1.10 (fixes CVE-2019-12781)
  see https://www.djangoproject.com/weblog/2019/jul/01/security-releases/
  for details


2.1.9.1 (2019-06-03)
====================

* Upgrade Django to 2.1.9 (fixes CVE-2019-12308)
  see https://www.djangoproject.com/weblog/2019/jun/03/security-releases/
  for details


2.1.8.1 (2019-04-09)
====================

* Add Django 2.1.8 support
* Replaced raven with sentry-sdk


2.1.7.1 (2019-02-11)
====================

* Upgrade Django to 2.1.7 (fixes CVE-2019-6975)
  see https://www.djangoproject.com/weblog/2019/feb/11/security-releases/
  for details
* Django 2.1.6 was faulty and is not provided on Divio Cloud, see
  https://code.djangoproject.com/ticket/30175 for details


2.1.5.3 (2019-01-29)
====================

* Added missing ``entry_points`` to ``setup.py``


2.1.5.2 (2019-01-29)
====================

* Added test matrix
* Adapted code base to align with other supported addons
* Allow users to configure aldryn sites redirect type via env variable


2.1.5.1 (2019-01-07)
====================

* Upgrade Django to 2.1.5 (fixes CVE-2019-3498)
  see https://www.djangoproject.com/weblog/2019/jan/04/security-releases/
  for details


2.1.4.1 (2018-12-17)
====================

* Add Django 2.1.4 support


2.1.2.1 (2018-10-01)
====================

* Add Django 2.1.2 support


2.1.1.1 (2018-09-17)
====================

* Add Django 2.1.1 support
