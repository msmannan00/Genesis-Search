from django.http import HttpResponseRedirect
from django.shortcuts import render

from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_MODEL_CALLBACK, MANAGE_STATUS_SESSION_COMMANDS
from Genesis.controllers.view_managers.cms.manage_status.manage_status_session_controller import manage_status_session_controller
from shared_directory.request_manager.request_handler import request_handler


class manage_status_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = manage_status_session_controller()
        pass

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(MANAGE_STATUS_SESSION_COMMANDS.M_INIT, p_data)
        if m_status is True:
            return render(None, CONSTANTS.S_TEMPLATE_MANAGE_STATUS_WEBSITE_PATH, m_context)
        else:
            return render(None, CONSTANTS.S_TEMPLATE_LOGIN_WEBSITE_PATH, m_context)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_STATUS_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
