# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url


if settings.ALDRYN_DJANGO_ENABLE_GIS:
    from django.contrib.gis import admin
else:
    from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
