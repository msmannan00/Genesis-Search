from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from app_manager.state_manager.states import APP_STATUS
from django.utils.deprecation import MiddlewareMixin

class MaintenanceModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if APP_STATUS.S_MAINTAINANCE is True:
            return render(request, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
        return None
