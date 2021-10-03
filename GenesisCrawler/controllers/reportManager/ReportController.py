
from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportModelCommands
from GenesisCrawler.controllers.reportManager.ReportModel import ReportModel
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class ReportController(RequestHandler):

    # Private Variables
    __instance = None
    __m_report_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if ReportController.__instance is None:
            ReportController()
        return ReportController.__instance

    def __init__(self):
        if ReportController.__instance is not None:
            raise Exception(ReportModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            ReportController.__instance = self
            self.__m_report_model = ReportModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ReportModelCommands.M_INIT:
            m_response, m_status = self.__m_report_model.invoke_trigger(ReportModelCommands.M_INIT, p_data)
            if m_status is not True:
                return render(None, constants.S_TEMPLATE_REPORT_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_TEMPLATE_NOTICE_WEBSITE_REPORT)
        else:
            m_response = None
        return m_response

