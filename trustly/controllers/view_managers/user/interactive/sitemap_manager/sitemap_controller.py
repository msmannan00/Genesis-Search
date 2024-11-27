from django.http import HttpResponseRedirect
from django.shortcuts import render

from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, SITEMAP_CALLBACK
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_model import sitemap_model
from app_manager.request_manager.request_handler import request_handler
from app_manager.state_manager.states import APP_STATUS


class sitemap_controller(request_handler):

    # Private Variables
    __instance = None
    __m_notice_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if sitemap_controller.__instance is None:
            sitemap_controller()
        return sitemap_controller.__instance

    def __init__(self):
        if sitemap_controller.__instance is not None:
            pass
        else:
            sitemap_controller.__instance = self
            self.__m_notice_model = sitemap_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_notice_model.invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, p_data)
            if m_status is False:
                return render(None, CONSTANTS.S_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_UPLOAD + "&mNoticeParamData=" + m_response[SITEMAP_CALLBACK.M_SECRETKEY])

