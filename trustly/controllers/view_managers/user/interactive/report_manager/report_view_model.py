
from django.http import HttpResponseRedirect
from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.report_manager.report_enums import REPORT_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.report_manager.report_model import report_model
from trustly.services.request_manager.request_handler import request_handler


class report_view_model(request_handler):

    # Private Variables
    __instance = None
    __m_report_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if report_view_model.__instance is None:
            report_view_model()
        return report_view_model.__instance

    def __init__(self):
        if report_view_model.__instance is not None:
            pass
        else:
            report_view_model.__instance = self
            self.__m_report_model = report_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_report_model.invoke_trigger(REPORT_MODEL_COMMANDS.M_INIT, p_data)
            if m_status is not True:
                return render(None, CONSTANTS.S_TEMPLATE_REPORT_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_REPORT)
        else:
            m_response = None
        return m_response

