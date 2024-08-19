from django.shortcuts import render

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_model import homepage_model
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND


class homepage_controller(request_handler):

    # Private Variables
    __instance = None
    __m_homepage_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if homepage_controller.__instance is None:
            homepage_controller()
        return homepage_controller.__instance

    def __init__(self):
        if homepage_controller.__instance is not None:
            pass
        else:
            homepage_controller.__instance = self
            self.__m_homepage_model = homepage_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_homepage_model.invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, p_data)
            return render(None, CONSTANTS.S_TEMPLATE_INDEX_PATH, m_response)
        else:
            m_response = None
        return m_response
