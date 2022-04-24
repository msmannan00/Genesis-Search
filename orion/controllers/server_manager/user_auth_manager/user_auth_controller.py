from django.http import HttpResponseRedirect
from django.shortcuts import render

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.constants.enums import MONGO_COMMANDS
from orion.controllers.server_manager.user_auth_manager.user_auth_enums import USER_AUTH_COMMANDS
from orion.controllers.server_manager.user_auth_manager.user_auth_session_controller import user_auth_session_controller
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.mongo_manager.mongo_controller import mongo_controller
from shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from shared_directory.service_manager.session.session_controller import session_controller
from shared_directory.service_manager.session.session_enums import SESSION_COMMANDS, SESSION_KEYS


class user_auth_controller(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    @staticmethod
    def getInstance():
        if user_auth_controller.__instance is None:
            user_auth_controller()
        return user_auth_controller.__instance

    def __init__(self):
        if user_auth_controller.__instance is not None:
            pass
        else:
            user_auth_controller.__instance = self
            self.__m_session = user_auth_session_controller()

    def __authenticate(self, p_data):

        m_user_model = self.__m_session.invoke_trigger(USER_AUTH_COMMANDS.M_INIT, p_data)

        if SESSION_KEYS.S_USERNAME in p_data.session:
            return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_DASHBOARD_WEBSITE_SHORT)
        else:
            if m_user_model.m_username is None or m_user_model.m_password is None:
                return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_LOGIN_SHORT)
            else:
                m_response, m_status = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_READ, [MONGO_COMMANDS.M_VERIFY_CREDENTIAL, [m_user_model.m_username, m_user_model.m_password], [None,None]])
                m_result = next(m_response, None)

                if m_result:
                    session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_CREATE, [m_user_model, p_data])
                    return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_DASHBOARD_WEBSITE_SHORT)
                else:
                    return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_LOGIN_SHORT+"?pError=true")

    def __logout(self, p_data):
        if SESSION_KEYS.S_USERNAME in p_data.session:
            del p_data.session[SESSION_KEYS.S_USERNAME]
            return HttpResponseRedirect(CONSTANTS.S_TEMPLATE_LOGIN_SHORT)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_AUTH_COMMANDS.M_AUTHENTICATE:
            return self.__authenticate(p_data)
        if p_command == USER_AUTH_COMMANDS.M_LOGOUT:
            return self.__logout(p_data)
