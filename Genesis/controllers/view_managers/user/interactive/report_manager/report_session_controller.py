from Genesis.controllers.constants.message import REPORT_MESSAGES
from Genesis.controllers.constants.strings import GENERAL_STRINGS
from Genesis.controllers.helper_manager.helper_controller import helper_controller
from Genesis.controllers.view_managers.user.interactive.report_manager.class_model.report_data_model import report_data_model
from Genesis.controllers.view_managers.user.interactive.report_manager.report_enums import REPORT_CALLBACK, REPORT_PARAM, REPORT_SESSION_COMMANDS
from shared_directory.request_manager.request_handler import request_handler


class report_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_report_data_model = report_data_model()
        if REPORT_PARAM.M_URL in p_data.POST:
            m_report_data_model.m_url = p_data.POST[REPORT_PARAM.M_URL]
        elif REPORT_PARAM.M_URL in p_data.GET:
            m_report_data_model.m_url = p_data.GET[REPORT_PARAM.M_URL]
        if REPORT_PARAM.M_EMAIL in p_data.POST:
            m_report_data_model.m_email = p_data.POST[REPORT_PARAM.M_EMAIL]
        if REPORT_PARAM.M_MESSAGE in p_data.POST:
            m_report_data_model.m_message = p_data.POST[REPORT_PARAM.M_MESSAGE]
        if REPORT_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_report_data_model.m_site = p_data.GET[REPORT_PARAM.M_SECURE_SERVICE]

        return m_report_data_model

    def init_callbacks(self, p_report_model:report_data_model):
        m_context_response = {
            REPORT_CALLBACK.M_URL: p_report_model.m_url,
            REPORT_CALLBACK.M_EMAIL: p_report_model.m_email,
            REPORT_CALLBACK.M_MESSAGE: p_report_model.m_message,
            REPORT_CALLBACK.M_URL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_EMAIL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_SECURE_SERVICE_NOTICE: p_report_model.m_site,
        }

        return m_context_response
    def __validate_parameters(self, p_report_data_model:report_data_model, p_data):
        m_validity_status = True
        if p_report_data_model.m_url is None:
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
        if REPORT_PARAM.M_URL not in p_data.POST:
            m_validity_status = False

        return p_report_data_model,m_context_response, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == REPORT_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0], p_data[1])

