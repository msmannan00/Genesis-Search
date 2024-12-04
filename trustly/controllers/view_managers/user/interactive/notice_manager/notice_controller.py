from django.http import HttpResponseRedirect
from django.shortcuts import render

from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_model import notice_model
from app_manager.request_manager.request_handler import request_handler
from app_manager.state_manager.states import APP_STATUS
from trustly.controllers.view_managers.user.server.error.error_controller import error_controller
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK


class notice_controller(request_handler):

    # Private Variables
    __instance = None
    __m_notice_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if notice_controller.__instance is None:
            notice_controller()
        return notice_controller.__instance

    def __init__(self):
        if notice_controller.__instance is not None:
            pass
        else:
            notice_controller.__instance = self
            self.__m_notice_model = notice_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NOTICE_MODEL_CALLBACK.M_INIT:
            m_response, m_status, m_browser = self.__m_notice_model.invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, p_data)
            if m_status is True:
                return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH, m_response)
            else:
                return error_controller.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [p_data, 404])