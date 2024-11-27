from app_manager.state_manager.states import APP_STATUS
from django.utils.deprecation import MiddlewareMixin
from trustly.controllers.view_managers.user.server.maintenance.maintenance_controller import maintenance_controller
from trustly.controllers.view_managers.user.server.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK


class maintenance_mode_middleware(MiddlewareMixin):
    def process_request(self, request):
        if APP_STATUS.S_MAINTAINANCE is True:
            return maintenance_controller.getInstance().invoke_trigger(MAINTENANCE_MODEL_CALLBACK.M_INIT, request)
