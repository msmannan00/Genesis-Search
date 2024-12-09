from trustly.services.state_manager.states import APP_STATUS
from django.utils.deprecation import MiddlewareMixin
from trustly.controllers.view_managers.user.server.maintenance.maintenance_view_model import maintenance_view_model
from trustly.controllers.view_managers.user.server.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK


class maintenance_mode_middleware(MiddlewareMixin):
  @staticmethod
  def process_request(request):
    if APP_STATUS.S_MAINTAINANCE is True:
      return maintenance_view_model.getInstance().invoke_trigger(MAINTENANCE_MODEL_CALLBACK.M_INIT, request)
