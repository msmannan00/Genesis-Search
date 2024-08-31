import uuid
from django.utils.deprecation import MiddlewareMixin

class cms_session_security(MiddlewareMixin):

    def process_request(self, request):
        session_token = request.session.get('session_token')
        browser_token = request.COOKIES.get('browser_session_token')

        if not session_token:
            session_token = uuid.uuid4().hex
            request.session['session_token'] = session_token

        if not browser_token or session_token != browser_token:
            request.session.flush()
            request.session['session_token'] = session_token

        request.session.modified = True

    def process_response(self, request, response):
        session_token = request.session.get('session_token')
        response.set_cookie('browser_session_token', session_token, max_age=600)
        return response
