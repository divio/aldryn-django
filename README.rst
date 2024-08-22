=============
Aldryn Django
=============

|pypi| |build| |coverage|

An opinionated Django setup bundled as a Divio Cloud addon.

This package will auto configure Django, including admin and some other basic
packages. It also handles sane configuration of the database connection and
static and media files.

The goal is to keep the footprint inside the Django website project as small
as possible, so updating things usually just means bumping a version in
``requirements.txt`` and no other changes in the project.

This addon still uses the legacy "Aldryn" naming. You can read more about this in our
`support section <https://support.divio.com/general/faq/essential-knowledge-what-is-aldryn>`_.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-django/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/aldryn-django/blob/master/setup.py>`_
file for additional dependencies:

|python| |django|


Installation
------------

Nothing to do. ``aldryn-django`` is part of the Divio Cloud platform.

For a manual install:

.. important::

    Please follow the setup instructions for installing
    ``aldryn-addons`` first!


Add ``aldryn-django`` to your projects ``requirements.txt`` or pip install it.

The version is made up of the Django release with an added digit for the
release version of this package itself.

If you followed the ``aldryn-addons`` installation instructions, you should
already have a ``ALDRYN_ADDONS`` setting. Add ``aldryn-django`` to it::

    INSTALLED_ADDONS = [
        'aldryn-django',
    ]

Create the ``addons/aldryn-django`` directory at the same level as your
``manage.py``. Then copy ``addon.json``, ``aldryn_config.py`` from
the matching sourcecode into it.

Also create a ``settings.json`` file in the same directory with the following
content::

    {
        "languages": "[\"en\", \"de\"]"
    }

.. Note:: The need to manually copy ``aldryn_config.py`` and ``addon.json`` is
          due to legacy compatibility with the Divio Cloud platform and will no
          longer be necessary in a later release of aldryn-addons.


Configuration
-------------

aldryn-django comes with entrypoints for ``manage.py`` and ``wsgi.py``. This
makes it possible to just have a small snippet of code in the website project
that should never change inside those files. The details of local project
setup (e.g reading environment variables from a ``.env`` file) are then up to
the currently installed version of ``aldryn-django``. Also other opinionated
things can be done, like using a production-grade wsgi middleware to serve
static and media files.


Put this in manage.py::

    #!/usr/bin/env python
    import os
    from aldryn_django import startup


    if __name__ == "__main__":
        startup.manage(path=os.path.dirname(os.path.abspath(__file__)))


put this in wsgi.py::

    import os
    from aldryn_django import startup


    application = startup.wsgi(path=os.path.dirname(__file__))


APIs
----

Migrations
**********

To run migrations, call the command ``aldryn-django migrate``. This will run
a series of commands for the migration stage of a project.

``aldryn-django`` will run ``python manage.py migrate``. But any addon
can add stuff to this migration step by appending commands to the ``MIGRATION_COMMANDS``
setting. For example ``aldryn-cms`` (django-cms as an Addon) will run
``python manage.py cms fix-tree`` at the migration stage.


Production Server
*****************

Calling ``aldryn-django web`` will start an opinionated Django setup for
production (currently uWSGI based).


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/aldryn-django.svg
    :target: http://badge.fury.io/py/aldryn-django
.. |build| image:: https://github.com/divio/aldryn-django/actions/workflows/default.yml/badge.svg?branch=support/5.1.x
    :target: https://github.com/divio/aldryn-django/actions
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-django/branch/support/5.1.x/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-django

.. |python| image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%C2%A03.12-blue.svg
    :target: https://pypi.org/project/aldryn-django/
.. |django| image:: https://img.shields.io/badge/django-5.1-blue.svg
    :target: https://www.djangoproject.com/
