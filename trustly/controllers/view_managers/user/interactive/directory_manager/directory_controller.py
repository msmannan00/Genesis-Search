
from django.shortcuts import render

from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_model import directory_model
from app_manager.request_manager.request_handler import request_handler
from app_manager.state_manager.states import APP_STATUS


class directory_controller(request_handler):

    # Private Variables
    __instance = None
    __m_directory_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if directory_controller.__instance is None:
            directory_controller()
        return directory_controller.__instance

    def __init__(self):
        if directory_controller.__instance is not None:
            pass
        else:
            directory_controller.__instance = self
            self.__m_directory_model = directory_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_MODEL_COMMANDS.M_INIT:
            m_response, m_status, m_360 = self.__m_directory_model.invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, p_data)
            return render(None, CONSTANTS.S_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
        else:
            m_response = None
        return m_response

