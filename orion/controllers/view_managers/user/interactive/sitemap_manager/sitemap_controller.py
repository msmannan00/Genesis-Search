from django.http import HttpResponseRedirect
from django.shortcuts import render

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, \
    SITEMAP_CALLBACK
from orion.controllers.view_managers.user.interactive.sitemap_manager.sitemap_model import sitemap_model
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.block_manager.block_controller import block_controller
from shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from shared_directory.state_manager.constant import APP_STATUS


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

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            if APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                m_response, m_status = self.__m_notice_model.invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, p_data)
                if m_status is False:
                    if "browser" in p_data.GET and p_data.GET["browser"] == "360wise":
                        return render(None, CONSTANTS.S_360_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
                    else:
                        return render(None, CONSTANTS.S_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
                else:
                    return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_UPLOAD + "&mNoticeParamData=" + m_response[SITEMAP_CALLBACK.M_SECRETKEY])

