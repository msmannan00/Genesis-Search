from django.http import HttpResponse
from django.shortcuts import render

from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.server.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK
from trustly.controllers.view_managers.user.server.user_index_manager.user_index_model import user_index_model
from app_manager.request_manager.request_handler import request_handler


class user_index_controller(request_handler):

    # Private Variables
    __instance = None
    __m_user_index_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if user_index_controller.__instance is None:
            user_index_controller()
        return user_index_controller.__instance

    def __init__(self):
        if user_index_controller.__instance is not None:
            pass
        else:
            user_index_controller.__instance = self
            self.__m_user_index_model = user_index_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_INDEX_MODEL_CALLBACK.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            else:
                return HttpResponse(self.__m_user_index_model.invoke_trigger(USER_INDEX_MODEL_CALLBACK.M_INIT, p_data))



