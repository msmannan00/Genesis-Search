import os

from django.utils.deprecation import MiddlewareMixin
from dotenv import load_dotenv

load_dotenv()


class content_security_policy_middleware(MiddlewareMixin):
    DEBUG = os.getenv("PRODUCTION", "0") != "1"

    def process_response(self, request, response):
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "frame-src 'none'; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "upgrade-insecure-requests; "
            "report-uri /csp-report-endpoint/; "
            "require-trusted-types-for 'script';"
        )

        if not self.DEBUG:
            response['Strict-Transport-Security'] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        response['Permissions-Policy'] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=(), "
            "fullscreen=(), "
            "xr-spatial-tracking=()"
        )

        return response