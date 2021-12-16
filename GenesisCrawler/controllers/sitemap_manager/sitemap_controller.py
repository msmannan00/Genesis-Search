from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constant import CONSTANTS
from GenesisCrawler.controllers.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, SITEMAP_CALLBACK
from GenesisCrawler.controllers.sitemap_manager.sitemap_model import sitemap_model


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

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_notice_model.invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, p_data)
            if m_status is False:
                return render(None, CONSTANTS.S_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_UPLOAD + "&mNoticeParamData=" + m_response[SITEMAP_CALLBACK.M_SECRETKEY])

