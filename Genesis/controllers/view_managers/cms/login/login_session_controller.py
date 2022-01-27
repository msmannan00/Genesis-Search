from Genesis.controllers.view_managers.cms.login.class_model.login_data_model import login_data_model
from Genesis.controllers.view_managers.cms.login.login_enums import LOGIN_PARAM, LOGIN_SESSION_COMMANDS, LOGIN_CALLBACK, \
    LOGIN_CALLBACK_MESSAGES
from shared_directory.request_manager.request_handler import request_handler


class login_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_login_model = login_data_model()

        if LOGIN_PARAM.M_ERROR in p_data.GET:
            m_login_model.m_error = LOGIN_CALLBACK_MESSAGES.M_LOGIN_FAILED

        return m_login_model

    def init_callbacks(self, p_report_model:login_data_model):
        m_context_response = {
            LOGIN_CALLBACK.M_ERROR: p_report_model.m_error
        }

        return m_context_response

    def __validate_parameters(self, p_login_data_model:login_data_model):
        m_context_response = self.init_callbacks(p_login_data_model)
        return m_context_response

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == LOGIN_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)
        if p_command == LOGIN_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data)

