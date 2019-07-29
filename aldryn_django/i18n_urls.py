# -*- coding: utf-8 -*-
import sys

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


if settings.ALDRYN_DJANGO_ENABLE_GIS:
    from django.contrib.gis import admin
else:
    from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# serve static files differently on local development
if setting.IS_RUNNING_DEVSERVER:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
