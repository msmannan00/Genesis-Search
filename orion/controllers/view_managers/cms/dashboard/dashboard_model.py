from django.http import HttpResponseRedirect
from django.shortcuts import render

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_SESSION_COMMANDS, DASHBOARD_MODEL_CALLBACK
from orion.controllers.view_managers.cms.dashboard.dashboard_session_controller import dashboard_session_controller
from shared_directory.request_manager.request_handler import request_handler

class dashboard_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = dashboard_session_controller()
        pass

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(DASHBOARD_SESSION_COMMANDS.M_INIT, p_data)
        if m_status is True:
            return render(None, CONSTANTS.S_TEMPLATE_DASHBOARD_WEBSITE_PATH, m_context)
        else:
            return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_LOGIN_SHORT)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == DASHBOARD_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
