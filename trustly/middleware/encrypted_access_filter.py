from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND


class EncryptedAccessFilter(MiddlewareMixin):
  def process_request(self, request):
    p_data = self.get_data_from_request(request)

    if not block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data):
      return HttpResponse("Unauthorized", status=401)

  def get_data_from_request(self, request):
    return request.POST.get('data', None)