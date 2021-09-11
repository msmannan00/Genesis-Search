
from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import ErrorMessages
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportModelCommands
from GenesisCrawler.controllers.reportManager.ReportModel import ReportModel

class ReportController:

    # Private Variables
    __instance = None
    mReportModel = None

    # Initializations
    @staticmethod
    def getInstance():
        if ReportController.__instance is None:
            ReportController()
        return ReportController.__instance

    def __init__(self):
        if ReportController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            ReportController.__instance = self
            self.mReportModel = ReportModel()

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == ReportModelCommands.M_INIT:
            m_response, mStatus = self.mReportModel.invokeTrigger(ReportModelCommands.M_INIT, pData)
            if mStatus is not True:
                return render(None, constants.S_REPORT_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_NOTICE_WEBSITE_REPORT_SUCCESS)
        else:
            m_response = None
        return m_response

