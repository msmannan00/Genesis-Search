from django.http import HttpResponseRedirect
from django.shortcuts import render

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.cms.login.login_enums import LOGIN_SESSION_COMMANDS, LOGIN_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.login.login_session_controller import login_session_controller
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.session.session_enums import SESSION_KEYS


class login_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = login_session_controller()
        pass

    def __init_page(self, p_data):
        if SESSION_KEYS.S_USERNAME in p_data.session :
            return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_DASHBOARD_WEBSITE_SHORT)
        else:
            m_login_data_model = self.__m_session.invoke_trigger(LOGIN_SESSION_COMMANDS.M_INIT, p_data)
            m_context = self.__m_session.invoke_trigger(LOGIN_SESSION_COMMANDS.M_VALIDATE, m_login_data_model)

            return render(None, CONSTANTS.S_TEMPLATE_LOGIN_WEBSITE_PATH, m_context)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == LOGIN_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
