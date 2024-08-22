from django.http import Http404

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ['/maintenance/', '/notice/', '/secretkey/', '/restricted/', '/logout/']
        if request.path in restricted_paths:
            if 'HTTP_REFERER' not in request.META:
                raise Http404("Page not found.")

        response = self.get_response(request)
        return response
