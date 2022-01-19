from django.shortcuts import render

from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.view_managers.server_views.error.error_enums import ERROR_MODEL_CALLBACK
from Genesis.controllers.view_managers.server_views.error.error_model import error_model


class error_controller:

    # Private Variables
    __instance = None
    __m_error_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if error_controller.__instance is None:
            error_controller()
        return error_controller.__instance

    def __init__(self):
        if error_controller.__instance is not None:
            pass
        else:
            error_controller.__instance = self
            self.__m_error_model = error_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ERROR_MODEL_CALLBACK.M_INIT:
            m_response, m_status = self.__m_error_model.invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, p_data)
            return render(None, CONSTANTS.S_TEMPLATE_ERROR_WEBSITE_PATH, m_response)

