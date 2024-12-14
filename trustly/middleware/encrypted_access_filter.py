from django.utils.deprecation import MiddlewareMixin

from trustly.app.view_managers.server.error.error_enums import ERROR_MODEL_CALLBACK
from trustly.services.block_manager.block_controller import block_controller
from trustly.services.block_manager.block_enums import BLOCK_COMMAND
from django.urls import resolve
from trustly.app.view_managers.server.error.error_view_model import error_view_model
from trustly.app.view_managers.server.maintenance.maintenance_view_model import maintenance_view_model
from trustly.app.view_managers.server.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK


class EncryptedAccessFilter(MiddlewareMixin):
  @staticmethod
  def process_request(request):
    allowed_paths = ['feeder', 'parser', 'feeder_publish', 'feeder_unique', 'update_status', 'crawl_index', 'cms']
    resolved_path = resolve(request.path_info).url_name

    if resolved_path in allowed_paths:
      if not block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, request):
        if resolved_path == 'cms':
          return maintenance_view_model.getInstance().invoke_trigger(MAINTENANCE_MODEL_CALLBACK.M_INIT, request)
        return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 404])
