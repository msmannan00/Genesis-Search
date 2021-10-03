from GenesisCrawler.constants import strings
from GenesisCrawler.constants.message import *
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportSessionCommands, ReportCallback, ReportParam
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class ReportSessionController(RequestHandler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_status = False
        __m_context = {
            ReportCallback.M_URL: strings.S_GENERAL_EMPTY,
            ReportCallback.M_EMAIL: strings.S_GENERAL_EMPTY,
            ReportCallback.M_MESSAGE: strings.S_GENERAL_EMPTY,
            ReportCallback.M_URL_ERROR: strings.S_GENERAL_EMPTY,
            ReportCallback.M_EMAIL_ERROR: strings.S_GENERAL_EMPTY,
            ReportCallback.M_URL_REDIRECTED: strings.S_GENERAL_EMPTY,
        }

        if p_data.POST is None:
            m_status = False
        if ReportParam.M_URL in p_data.POST:
            __m_context[ReportCallback.M_URL] = p_data.POST[ReportParam.M_URL]
            m_status = True
        if len(p_data.POST) == 0 and ReportParam.M_URL in p_data.GET:
            __m_context[ReportCallback.M_URL_REDIRECTED] = p_data.GET[ReportParam.M_URL]
            m_status = True
        if ReportParam.M_EMAIL in p_data.POST:
            __m_context[ReportCallback.M_EMAIL] = p_data.POST[ReportParam.M_EMAIL]
            m_status = True
        if ReportParam.M_MESSAGE in p_data.POST:
            __m_context[ReportCallback.M_MESSAGE] = p_data.POST[ReportParam.M_MESSAGE]
            m_status = True

        return __m_context, m_status

    def __validate_parameters(self, p_context):
        m_validity_status = True

        if p_context[ReportCallback.M_URL_REDIRECTED] == strings.S_GENERAL_EMPTY:
            if p_context[ReportCallback.M_URL] == strings.S_GENERAL_EMPTY:
                p_context[ReportCallback.M_URL_ERROR] = S_REPORT_URL_INCOMPLETE_ERROR
                m_validity_status = False
            if p_context[ReportCallback.M_URL].startswith(strings.S_GENERAL_HTTP) is False:
                p_context[ReportCallback.M_URL_ERROR] = S_REPORT_URL_INVALID_PROTOCOL
                m_validity_status = False
            elif HelperController.isURLValid(p_context[ReportCallback.M_URL]) is False or HelperController.getHost(p_context[ReportCallback.M_URL]).__contains__(strings.S_GENERAL_ONION_DOMAIN) is False:
                p_context[ReportCallback.M_URL_ERROR] = S_REPORT_URL_INVALID_ERROR
                m_validity_status = False
        else:
            m_validity_status = False

        if p_context[ReportCallback.M_EMAIL] != strings.S_GENERAL_EMPTY and HelperController.isMailValid(p_context[ReportCallback.M_EMAIL]) is False:
            p_context[ReportCallback.M_EMAIL_ERROR] = S_REPORT_URL_INVALID_EMAIL
            m_validity_status = False

        return p_context, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ReportSessionCommands.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == ReportSessionCommands.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

