from django.http import HttpResponseRedirect
from django.shortcuts import render
from genesis_server.controllers.constants.constant import CONSTANTS, APP_STATUS
from genesis_shared_directory.service_manager.block_manager.block_controller import block_controller
from genesis_shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from genesis_server.controllers.view_managers.user_views.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, SITEMAP_CALLBACK
from genesis_server.controllers.view_managers.user_views.sitemap_manager.sitemap_model import sitemap_model
from genesis_shared_directory.state_manager.server_vars import SERVER_VARS


class sitemap_controller:

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
            raise Exception(SITEMAP_MODEL_COMMANDS.ErrorMessages.M_SINGLETON_EXCEPTION)
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
            elif APP_STATUS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                m_response, m_status = self.__m_notice_model.invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, p_data)
                if m_status is False:
                    return render(None, CONSTANTS.S_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
                else:
                    return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_UPLOAD + "&mNoticeParamData=" + m_response[SITEMAP_CALLBACK.M_SECRETKEY])

