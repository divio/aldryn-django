from django.urls import re_path, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
]
