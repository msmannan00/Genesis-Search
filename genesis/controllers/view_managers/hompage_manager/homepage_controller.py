from django.shortcuts import render

from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.service_manager.block_manager.block_controller import block_controller
from genesis.controllers.service_manager.block_manager.block_enums import BLOCK_COMMAND
from genesis.controllers.view_managers.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from genesis.controllers.view_managers.hompage_manager.homepage_model import homepage_model


class homepage_controller:

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
            raise Exception(HOMEPAGE_MODEL_COMMANDS.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            homepage_controller.__instance = self
            self.__m_homepage_model = homepage_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_homepage_model.invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, None)
            return render(None, CONSTANTS.S_TEMPLATE_INDEX_PATH, m_response)
        else:
            m_response = None
        return m_response
