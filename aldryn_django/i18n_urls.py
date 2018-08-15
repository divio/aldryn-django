from django.conf import settings
from django.urls import re_path

if settings.ALDRYN_DJANGO_ENABLE_GIS:
    from django.contrib.gis import admin
else:
    from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
]
