# -*- coding: utf-8 -*-
import os
import sys
from getenv import env
import django.core.management


def manage(path):
    _setup(path=path)
    utility = django.core.management.ManagementUtility(None)
    utility.execute()


def wsgi(path):
    _setup(path=path)
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from dj_static import Cling, MediaCling
    app = get_wsgi_application()
    if settings.ENABLE_SYNCING:
        if not settings.STATIC_URL_IS_ON_OTHER_DOMAIN:
            app = Cling(app)
        if not settings.MEDIA_URL_IS_ON_OTHER_DOMAIN:
            app = MediaCling(app)
    return app


def _setup(path):
    os.environ['DJANGO_SETTINGS_MODULE'] = env('DJANGO_SETTINGS_MODULE', 'settings')
