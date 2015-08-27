# -*- coding: utf-8 -*-


# copied from django 1.7a2: https://github.com/django/django/blob/1.7a2/django/contrib/sites/middleware.py
from django.contrib.sites.models import Site


class CurrentSiteMiddleware(object):
    """
    Middleware that sets `site` attribute to request object.
    """

    def process_request(self, request):
        request.site = Site.objects.get_current()
