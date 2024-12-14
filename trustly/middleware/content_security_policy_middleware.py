from django.utils.deprecation import MiddlewareMixin


class content_security_policy_middleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "form-action 'self'; "
            "base-uri 'none'; "
        )
        return response
