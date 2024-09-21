from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from django.utils.deprecation import MiddlewareMixin
from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND


class EncryptedAccessFilter(MiddlewareMixin):
  def process_request(self, request):
    allowed_paths = ['/feeder', '/parser']
    if request.path in allowed_paths:
      if not block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, request):
        return render(request, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
