
from django.shortcuts import render

from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.service_manager.block_manager.block_controller import block_controller
from genesis.controllers.service_manager.block_manager.block_enums import BLOCK_COMMAND
from genesis.controllers.view_managers.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from genesis.controllers.view_managers.directory_manager.directory_model import directory_model


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

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_MODEL_COMMANDS.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)

            m_response, m_status = self.__m_directory_model.invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, p_data)
            if m_status is not True:
                return render(None, CONSTANTS.S_TEMPLATE_INDEX_PATH, m_response)
            else:
                return render(None, CONSTANTS.S_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
        else:
            m_response = None
        return m_response

