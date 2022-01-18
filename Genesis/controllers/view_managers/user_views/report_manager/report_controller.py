
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Genesis.controllers.constants.constant import CONSTANTS, APP_STATUS
from Genesis.controllers.view_managers.user_views.report_manager.report_enums import REPORT_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.report_manager.report_model import report_model
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND


class report_controller(request_handler):

    # Private Variables
    __instance = None
    __m_report_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if report_controller.__instance is None:
            report_controller()
        return report_controller.__instance

    def __init__(self):
        if report_controller.__instance is not None:
            pass
        else:
            report_controller.__instance = self
            self.__m_report_model = report_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_MODEL_COMMANDS.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            elif APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                m_response, m_status = self.__m_report_model.invoke_trigger(REPORT_MODEL_COMMANDS.M_INIT, p_data)
                if m_status is not True:
                    return render(None, CONSTANTS.S_TEMPLATE_REPORT_WEBSITE_PATH, m_response)
                else:
                    return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_REPORT)
        else:
            m_response = None
        return m_response

