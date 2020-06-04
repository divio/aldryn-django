=========
Changelog
=========


2.2.13.1 (2020-06-04)
=====================

* Upgrade Django to 2.2.13 (fixes CVE-2020-13254, CVE-2020-13596)
  see https://www.djangoproject.com/weblog/2020/jun/03/security-releases/
  for details


2.2.12.1 (2020-04-06)
=====================

* Add Django 2.2.12 support


2.2.11.2 (2020-03-13)
=====================

* Allow ``SITE_ID`` to be set through an environment variable


2.2.11.1 (2020-03-09)
=====================

* Upgrade Django to 2.2.11 (fixes CVE-2020-9402)
  see https://www.djangoproject.com/weblog/2020/mar/04/security-releases/
  for details


2.2.10.1 (2020-02-03)
=====================

* Upgrade Django to 2.2.10 (fixes CVE-2020-7471)
  see https://www.djangoproject.com/weblog/2020/feb/03/security-releases/
  for details
* Limit django-storages to < 1.9 until we switch to the new Boto3 S3 storage
  backend


2.2.9.1 (2019-12-03)
====================

* Upgrade Django to 2.2.9 (fixes CVE-2019-19844)
  see https://www.djangoproject.com/weblog/2019/dec/18/security-releases/
  for details


2.2.8.1 (2019-12-03)
====================

* Upgrade Django to 2.2.8
  (fixes CVE-2019-19118)
  see https://www.djangoproject.com/weblog/2019/dec/02/security-releases/
  for details


2.2.7.2 (2019-11-12)
====================

* Added the ``--need-app`` command line flag to the uwsgi startup options


2.2.7.1 (2019-11-04)
====================

* Add Django 2.2.7 support


2.2.6.1 (2019-10-08)
====================

* Add Django 2.2.6 support


2.2.5.1 (2019-09-24)
====================

* Add Django 2.2.5 support


2.2.4.1 (2019-08-05)
====================

* Upgrade Django to 2.2.4
  (fixes CVE-2019-14232, CVE-2019-14233, CVE-2019-14234, CVE-2019-14235)
  see https://www.djangoproject.com/weblog/2019/aug/01/security-releases/
  for details


2.2.3.4 (2019-07-29)
====================

* Serve static files from ``django.conf.urls.static`` during local development


2.2.3.3 (2019-07-24)
====================

* Removed ``ENABLE_SYNCING`` and thus serving files always from uwsgi
* Removed dj-static requirement and relevant code


2.2.3.2 (2019-07-16)
====================

 * Removed faulty help text for languages settings


2.2.3.1 (2019-07-01)
====================

* Upgrade Django to 2.2.3 (fixes CVE-2019-12781)
  see https://www.djangoproject.com/weblog/2019/jul/01/security-releases/
  for details


2.2.2.1 (2019-06-03)
====================

* Upgrade Django to 2.2.2 (fixes CVE-2019-12308)
  see https://www.djangoproject.com/weblog/2019/jun/03/security-releases/
  for details


2.2.1.1 (2019-05-13)
====================

* Add Django 2.2.1 support


2.2.0.4 (2019-04-09)
====================

* Added final release
* Replaced raven with sentry-sdk


2.2.0.3 (2019-03-21)
====================

* Added RC1 release


2.2.0.2 (2019-02-11)
====================

* Added beta 1 release


2.2.0.1 (2019-02-06)
====================

* Added alpha 1 release
