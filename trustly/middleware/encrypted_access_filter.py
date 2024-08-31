from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from django.utils.deprecation import MiddlewareMixin
from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND

class EncryptedAccessFilter(MiddlewareMixin):
    def process_request(self, request):
        p_data = self.get_data_from_request(request)
        if p_data is None or not block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data):
            print(":::::::::::::::::::::::::::::::::::::::::::::::::")
            return render(request, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)

    def get_data_from_request(self, request):
        return request.GET.get('data', None)
