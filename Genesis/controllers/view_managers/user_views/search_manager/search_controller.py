from django.http import HttpResponseRedirect
from django.shortcuts import render

from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.view_managers.user_views.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.search_manager.search_model import search_model
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from shared_directory.state_manager.constant import APP_STATUS


class search_controller:

    # Private Variables
    __instance = None
    __m_search_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if search_controller.__instance is None:
            search_controller()
        return search_controller.__instance

    def __init__(self):
        if search_controller.__instance is not None:
            pass
        else:
            search_controller.__instance = self
            self.__m_search_model = search_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_COMMANDS.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            elif APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                m_status, m_response = self.__m_search_model.invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, p_data)
                if m_status is True:
                    return render(None, CONSTANTS.S_TEMPLATE_SEARCH_WEBSITE_PATH, m_response)
                else:
                    return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_PARENT)
        else:
            m_response = None

        return m_response
