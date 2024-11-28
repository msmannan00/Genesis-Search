from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_CALLBACK, ERROR_SESSION_COMMANDS, \
    ERROR_PARAM, ERROR_MESSAGE_CALLBACK
from trustly.services.request_manager.request_handler import request_handler


class error_session_controller(request_handler):

    # Helper Methods
    @staticmethod
    def __init_parameters(p_data):
        m_param_data = p_data[0]
        m_error_code = p_data[1]

        m_context = {
            ERROR_CALLBACK.M_SECURE_SERVICE_NOTICE:"http",
            ERROR_CALLBACK.M_ERROR_CODE: m_error_code,
            ERROR_CALLBACK.M_ERROR_MESSAGE: GENERAL_STRINGS.S_GENERAL_EMPTY,
        }

        if ERROR_PARAM.M_SECURE_SERVICE in m_param_data.GET:
            m_context[ERROR_CALLBACK.M_SECURE_SERVICE_NOTICE] = m_param_data.GET[ERROR_PARAM.M_SECURE_SERVICE]

        if m_error_code == 400:
            m_context[ERROR_CALLBACK.M_ERROR_MESSAGE] = ERROR_MESSAGE_CALLBACK.M_ERROR_400
        if m_error_code == 403:
            m_context[ERROR_CALLBACK.M_ERROR_MESSAGE] = ERROR_MESSAGE_CALLBACK.M_ERROR_403
        if m_error_code == 404:
            m_context[ERROR_CALLBACK.M_ERROR_MESSAGE] = ERROR_MESSAGE_CALLBACK.M_ERROR_404
        if m_error_code == 500:
            m_context[ERROR_CALLBACK.M_ERROR_MESSAGE] = ERROR_MESSAGE_CALLBACK.M_ERROR_500

        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ERROR_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)

