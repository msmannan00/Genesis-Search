from trustly.services.session_manager.session_controller import session_controller
from trustly.services.session_manager.session_enums import SESSION_COMMANDS
from django.utils.deprecation import MiddlewareMixin
from trustly.services.block_manager.block_controller import block_controller
from trustly.services.block_manager.block_enums import BLOCK_COMMAND
from django.urls import resolve
from trustly.controllers.view_managers.user.server.error.error_view_model import error_view_model
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK


class EncryptedAccessFilter(MiddlewareMixin):
  @staticmethod
  def process_request(request):
    allowed_paths = ['feeder', 'parser', 'feeder_publish', 'feeder_unique', 'update_status', 'crawl_index']
    resolved_path = resolve(request.path_info).url_name
    m_status = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS, request)
    if not m_status and resolved_path in allowed_paths:
      if not block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, request):
        return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 404])
