=========
Changelog
=========


3.0.3.1 (2020-02-03)
====================

* Upgrade Django to 3.0.3 (fixes CVE-2020-7471)
  see https://www.djangoproject.com/weblog/2020/feb/03/security-releases/
  for details
* Limit django-storages to < 1.9 until we switch to the new Boto3 S3 storage
  backend


3.0.2.2 (2020-01-29)
====================

* Set Django ``X_FRAME_OPTIONS`` default to ``SAMEORIGIN``


3.0.2.1 (2020-01-06)
====================

* Add Django 3.0.2 support


3.0.1.1 (2019-12-03)
====================

* Upgrade Django to 3.0.1 (fixes CVE-2019-19844)
  see https://www.djangoproject.com/weblog/2019/dec/18/security-releases/
  for details


3.0.0.1 (2019-12-03)
====================

* Add Django 3.0 support


3.0.0.1.rc1 (2019-11-21)
========================

* Add Django 3.0rc1 (release candidate 1) support
* Added the ``--need-app`` command line flag to the uwsgi startup options


3.0.0.1.b1 (2019-10-21)
=======================

* Add Django 3.0b1 (beta 1) support


3.0.0.1.a1 (internal)
=====================

* Add Django 3.0a1 (alpha 1) support
