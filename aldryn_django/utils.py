from django.conf import settings
from django.conf.urls.i18n import i18n_patterns as django_i18n_patterns


def i18n_patterns(*args):
    """
    We want to avoid having to change anything in the projects
    root urls.py when new versions of Django are released.
    """
    use_prefix = getattr(settings, 'PREFIX_DEFAULT_LANGUAGE', True)
    return django_i18n_patterns(*args, prefix_default_language=use_prefix)
