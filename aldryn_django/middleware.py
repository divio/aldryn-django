from django.conf import settings


class RandomCommentExclusionMiddleware(object):
    def process_response(self, request, response):
        if not request.resolver_match:
            return response
        func_path = request.resolver_match._func_path
        if func_path in getattr(settings, 'RANDOM_COMMENT_EXCLUDED_VIEWS', []):
            response._random_comment_exempt = True
        return response
