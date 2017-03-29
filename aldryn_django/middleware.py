from django.conf import settings
from django.core.urlresolvers import is_valid_path, get_script_prefix
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import get_language_from_path


class LanguagePrefixFallbackMiddleware(MiddlewareMixin):
    """
    Redirects urls which raise a 404 and contain a language prefix
    that matches the default language to their non-language prefix
    version.
    """

    response_redirect_class = HttpResponseRedirect

    def strip_language(self, path):
        language_prefix = get_language_from_path(path)

        if not language_prefix:
            return path
        return "/" + "/".join(path.split("/")[2:])

    def process_response(self, request, response):
        language_from_path = get_language_from_path(request.path_info)

        if response.status_code == 404 and language_from_path == settings.LANGUAGE_CODE:
            urlconf = getattr(request, 'urlconf', None)
            new_path = self.strip_language(request.path_info)
            path_valid = is_valid_path(new_path, urlconf)

            if (not path_valid and settings.APPEND_SLASH and not new_path.endswith('/')):
                path_valid = is_valid_path("%s/" % new_path, urlconf)

            if path_valid:
                script_prefix = get_script_prefix()
                old_path = get_script_prefix() + language_from_path + '/'
                language_url = "%s://%s%s" % (
                    request.scheme,
                    request.get_host(),
                    # replace the old path which contains language code
                    # to the script prefix without language code
                    request.get_full_path().replace(old_path, script_prefix, 1)
                )
                return self.response_redirect_class(language_url)
        return response
