
from django.shortcuts import render
from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.view_managers.user.interactive.intelligence_manager.intelligence_enums import INTELLIGENCE_MODEL_COMMANDS
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from shared_directory.state_manager.constant import APP_STATUS


class intelligence_controller(request_handler):

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if intelligence_controller.__instance is None:
            intelligence_controller()
        return intelligence_controller.__instance

    def __init__(self):
        if intelligence_controller.__instance is not None:
            pass
        else:
            intelligence_controller.__instance = self

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == INTELLIGENCE_MODEL_COMMANDS.M_INIT:
            # if self.__on_verify_app(p_data) is True:
            #     return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            if APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                return render(None, CONSTANTS.S_TEMPLATE_INTELLIGENCE_WEBSITE_PATH)
        else:
            m_response = None
        return m_response

