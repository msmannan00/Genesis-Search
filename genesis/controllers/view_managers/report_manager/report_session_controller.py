from genesis.controllers.constants.message import *
from genesis.controllers.constants.strings import GENERAL_STRINGS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.view_managers.report_manager.report_enums import REPORT_SESSION_COMMANDS, REPORT_CALLBACK, REPORT_PARAM
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.shared_model.report_data_model import report_data_model


class report_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_report_data_model = report_data_model()
        if REPORT_PARAM.M_URL in p_data.POST:
            m_report_data_model.m_url = p_data.POST[REPORT_PARAM.M_URL]
            print("1------------------", flush=True)
        if REPORT_PARAM.M_EMAIL in p_data.POST:
            m_report_data_model.m_email = p_data.POST[REPORT_PARAM.M_EMAIL]
            print("2------------------", flush=True)
        if REPORT_PARAM.M_MESSAGE in p_data.POST:
            m_report_data_model.m_message = p_data.POST[REPORT_PARAM.M_MESSAGE]
            print("3------------------",flush=True)

        return m_report_data_model

    def init_callbacks(self, p_report_model:report_data_model):
        m_context_response = {
            REPORT_CALLBACK.M_URL: p_report_model.m_url,
            REPORT_CALLBACK.M_EMAIL: p_report_model.m_email,
            REPORT_CALLBACK.M_MESSAGE: p_report_model.m_message,
            REPORT_CALLBACK.M_URL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_EMAIL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
        }

        return m_context_response
    def __validate_parameters(self, p_report_data_model:report_data_model):
        m_validity_status = True
        if p_report_data_model.m_url is None or p_report_data_model.m_message is None:
            p_report_data_model.set_defaults()
            m_context_response = self.init_callbacks(p_report_data_model)
            return p_report_data_model, m_context_response, False

        m_context_response = self.init_callbacks(p_report_data_model)
        if p_report_data_model.m_url == GENERAL_STRINGS.S_GENERAL_EMPTY:
            m_context_response[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INCOMPLETE_ERROR
            m_validity_status = False
        if p_report_data_model.m_url.startswith(GENERAL_STRINGS.S_GENERAL_HTTP) is False:
            m_context_response[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_PROTOCOL
            m_validity_status = False
        elif helper_controller.is_url_valid(p_report_data_model.m_url) is False or helper_controller.get_host(p_report_data_model.m_url).__contains__(GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN) is False:
            m_context_response[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_ERROR
            m_validity_status = False

        if p_report_data_model.m_email != GENERAL_STRINGS.S_GENERAL_EMPTY and helper_controller.is_mail_valid(p_report_data_model.m_email) is False:
            m_context_response[REPORT_CALLBACK.M_EMAIL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_EMAIL
            m_validity_status = False

        return p_report_data_model,m_context_response, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == REPORT_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

