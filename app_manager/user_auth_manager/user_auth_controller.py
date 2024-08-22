import os

from django.http import HttpResponseRedirect

from app_manager.session_manager.session_controller import session_controller
from app_manager.session_manager.session_enums import SESSION_COMMANDS, SESSION_KEYS
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.enums import MONGO_COMMANDS
from app_manager.user_auth_manager.user_auth_enums import USER_AUTH_COMMANDS, USER_DATA
from app_manager.user_auth_manager.user_auth_session_controller import user_auth_session_controller
from app_manager.request_manager.request_handler import request_handler
from app_manager.mongo_manager.mongo_controller import mongo_controller
from app_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from dotenv import load_dotenv

load_dotenv()

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

                if m_result or m_user_model.m_username == USER_DATA.M_DEFAULT_USERNAME and m_user_model.m_password == os.getenv('S_SUPER_PASSWORD'):
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
