from trustly.controllers.view_managers.cms.login.login_enums import LOGIN_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.login.login_model import login_model


class login_view_model:

    # Private Variables
    __instance = None
    __m_login_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if login_view_model.__instance is None:
            login_view_model()
        return login_view_model.__instance

    def __init__(self):
        if login_view_model.__instance is not None:
            pass
        else:
            login_view_model.__instance = self
            self.__m_login_model = login_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == LOGIN_MODEL_CALLBACK.M_INIT:
            m_redirection = self.__m_login_model.invoke_trigger(LOGIN_MODEL_CALLBACK.M_INIT, p_data)
            return m_redirection
