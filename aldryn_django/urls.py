# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = [

]

# static/media serving is not needed here anymore, since we use the wsgi app
# for runserver as well (WSGI_APPLICATION setting).
# And that comes with dj-static to serve MEDIA and STATIC.
# urlpatterns += [
#     url(
#         r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
#         'django.contrib.staticfiles.views.serve',
#         {'insecure': True}
#     ),
#     url(
#         r'^favicon.ico$',
#         'django.contrib.staticfiles.views.serve',
#         {'insecure': True, 'path': 'favicon.ico'}
#     ),
# ]
#
# if not settings.MEDIA_URL_IS_ON_OTHER_DOMAIN:
#     urlpatterns += [
#         url(
#             r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
#             'django.views.static.serve',
#             {
#                 'document_root': settings.MEDIA_ROOT,
#             }
#         ),
#     ]
