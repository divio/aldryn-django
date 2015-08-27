#############
Aldryn Django
#############


|PyPI Version|

An opinionated Django setup bundled as an Aldryn Addon.

This package will auto configure Django, including admin and some other basic
packages. It also handles sane configuration of the database connection and
static and media files.

The goal is to keep the footprint inside the django website project as small
as possible, so updating things usually just means bumping a version in
``requirements.txt`` and no other changes in the project.

======================
Installation & Updates
======================

*********************
Aldryn Platform Users
*********************

Nothing to do. ``aldryn-django`` is part of the Aldryn Platform.

*******************
Manual Installation
*******************

.. important:: Please follow the setup instructions for installing
               ``aldryn-addons`` first!


Add ``aldryn-django`` to your projects ``requirements.txt`` or pip install it.
::

    pip install aldryn-django==1.6.11.1


The version is made up of the Django release with an added digit for the
release version of this package itself.

If you followed the ``aldryn-addons`` installation instructions, you should
already have a ``ALDRYN_ADDONS`` setting. Add ``aldryn-django`` to it.::

    INSTALLED_ADDONS = [
        'aldryn-django',
    ]

Create the ``addons/aldryn-django`` directory at the same level as your
``manage.py``. Then copy ``addon.json``, ``aldryn_config.py`` from
the matching sourcecode into it.
Also create a ``settings.json`` file in the same directory with the follwing
content::

    {
        "languages": "[\"en\", \"de\"]"
    }

.. Note:: The need to manually copy ``aldryn_config.py`` and ``addon.json`` is
          due to legacy compatibility with the Aldryn Platform and will no
          longer be necessary in a later release of aldryn-addons.


manage.py and wsgi.py
=====================

Aldryn django comes with entrypoints for ``manage.py`` and ``wsgi.py``. This
makes it possible to just have a small snippet of code in the website project
that should never change inside those files. The details of local project
setup (e.g reading environment variables from a ``.env`` file) are then up to
the currently installed version of ``aldryn-django``. Also other opinionated
things can be done, like using a production-grade wsgi middleware to serve
static and media files.


put this in manage.py::

    #!/usr/bin/env python
    import os
    from aldryn_django import startup


    if __name__ == "__main__":
        startup.manage(path=os.path.dirname(os.path.abspath(__file__)))


put this in wsgi.py::

    import os
    from aldryn_django import startup


    application = startup.wsgi(path=os.path.dirname(__file__))


====
APIs
====

**********
Migrations
**********

To run migrations, call the command ``aldryn-django migrate``. This will run
a series of commands for the migration stage of a project.
``aldryn-django`` will run ``python manage.py syncdb`` and
``python manage.py migrate`` (and on Django>=1.7 just
``python manage.py migrate``). But any Addon can add stuff to this migration
step by appending commands to the ``MIGRATION_COMMANDS`` setting. For example
``aldryn-cms`` (django-cms as an Addon) will run
``python manage.py cms fix-tree`` at the migration stage.


*****************
Production Server
*****************

Calling ``aldryn-django web`` will start an opinionated Django setup for
production (currently uwsgi based).


============
Contributing
============

This is a community project. We love to get any feedback in the form of
`issues`_ and `pull requests`_. Before submitting your pull request, please
review our guidelines for `Aldryn addons`_.

.. _issues: https://github.com/aldryn/aldryn-django/issues
.. _pull requests: https://github.com/aldryn/aldryn-django/pulls
.. _Aldryn addons: http://docs.aldryn.com/en/latest/reference/addons/index.html
.. _aldryn-django: https://github.com/aldryn/aldryn-django

.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-django.svg
   :target: https://pypi.python.org/pypi/aldryn-django
