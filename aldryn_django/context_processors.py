from django.conf import settings


def debug(request):
    # we don't use django.core.context_processors.debug because
    # it does not set True for ip that are not in INTERNAL_IPS
    return {'debug': settings.DEBUG}
