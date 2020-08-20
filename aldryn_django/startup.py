import os

import django.core.management

from getenv import env


def manage(path):
    _setup(path=path)
    utility = django.core.management.ManagementUtility(None)
    utility.execute()


def wsgi(path):
    _setup(path=path)
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
    return app


def setup(path):
    _setup(path)
    import django
    django.setup()


def _setup(path):
    os.environ['DJANGO_SETTINGS_MODULE'] = env(
        'DJANGO_SETTINGS_MODULE', 'settings'
    )
