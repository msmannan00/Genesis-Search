from GenesisCrawler.constants.message import *
from GenesisCrawler.constants.strings import GENERAL_STRINGS
from GenesisCrawler.controllers.helper_manager.helper_controller import helper_controller
from GenesisCrawler.controllers.report_manager.report_enums import REPORT_SESSION_COMMANDS, REPORT_CALLBACK, REPORT_PARAM
from GenesisCrawler.controllers.shared_model.request_handler import request_handler


class report_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_status = False
        __m_context = {
            REPORT_CALLBACK.M_URL: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_EMAIL: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_MESSAGE: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_URL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_EMAIL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            REPORT_CALLBACK.M_URL_REDIRECTED: GENERAL_STRINGS.S_GENERAL_EMPTY,
        }

        if p_data.POST is None:
            m_status = False
        if REPORT_PARAM.M_URL in p_data.POST:
            __m_context[REPORT_CALLBACK.M_URL] = p_data.POST[REPORT_PARAM.M_URL]
            m_status = True
        if len(p_data.POST) == 0 and REPORT_PARAM.M_URL in p_data.GET:
            __m_context[REPORT_CALLBACK.M_URL_REDIRECTED] = p_data.GET[REPORT_PARAM.M_URL]
            m_status = True
        if REPORT_PARAM.M_EMAIL in p_data.POST:
            __m_context[REPORT_CALLBACK.M_EMAIL] = p_data.POST[REPORT_PARAM.M_EMAIL]
            m_status = True
        if REPORT_PARAM.M_MESSAGE in p_data.POST:
            __m_context[REPORT_CALLBACK.M_MESSAGE] = p_data.POST[REPORT_PARAM.M_MESSAGE]
            m_status = True

        return __m_context, m_status

    def __validate_parameters(self, p_context):
        m_validity_status = True

        if p_context[REPORT_CALLBACK.M_URL_REDIRECTED] == GENERAL_STRINGS.S_GENERAL_EMPTY:
            if p_context[REPORT_CALLBACK.M_URL] == GENERAL_STRINGS.S_GENERAL_EMPTY:
                p_context[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INCOMPLETE_ERROR
                m_validity_status = False
            if p_context[REPORT_CALLBACK.M_URL].startswith(GENERAL_STRINGS.S_GENERAL_HTTP) is False:
                p_context[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_PROTOCOL
                m_validity_status = False
            elif helper_controller.is_url_valid(p_context[REPORT_CALLBACK.M_URL]) is False or helper_controller.get_host(p_context[REPORT_CALLBACK.M_URL]).__contains__(GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN) is False:
                p_context[REPORT_CALLBACK.M_URL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_ERROR
                m_validity_status = False
        else:
            m_validity_status = False

        if p_context[REPORT_CALLBACK.M_EMAIL] != GENERAL_STRINGS.S_GENERAL_EMPTY and helper_controller.is_mail_valid(p_context[REPORT_CALLBACK.M_EMAIL]) is False:
            p_context[REPORT_CALLBACK.M_EMAIL_ERROR] = REPORT_MESSAGES.S_REPORT_URL_INVALID_EMAIL
            m_validity_status = False

        return p_context, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == REPORT_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

