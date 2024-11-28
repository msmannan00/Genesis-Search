from django.shortcuts import render

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK
from trustly.controllers.view_managers.user.server.error.error_model import error_model
from trustly.services.request_manager.request_handler import request_handler


class error_view_model(request_handler):

    # Private Variables
    __instance = None
    __m_error_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if error_view_model.__instance is None:
            error_view_model()
        return error_view_model.__instance

    def __init__(self):
        if error_view_model.__instance is not None:
            pass
        else:
            error_view_model.__instance = self
            self.__m_error_model = error_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ERROR_MODEL_CALLBACK.M_INIT:
            m_response, m_status = self.__m_error_model.invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, p_data)
            return render(None, CONSTANTS.S_TEMPLATE_ERROR_WEBSITE_PATH, m_response, status=m_response['mErrorCode'])
