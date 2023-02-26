
from django.shortcuts import render

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.directory_manager.directory_model import directory_model
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from shared_directory.state_manager.constant import APP_STATUS


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
            #if self.__on_verify_app(p_data) is True:
            #    return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            elif APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                m_response, m_status, m_360 = self.__m_directory_model.invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, p_data)
                if m_status is not True:
                    return render(None, CONSTANTS.S_TEMPLATE_INDEX_PATH, m_response)
                else:
                    if m_360:
                        return render(None, CONSTANTS.S_360_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
                    else:
                        return render(None, CONSTANTS.S_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
        else:
            m_response = None
        return m_response

