import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapModelCommands, SitemapCallback
from GenesisCrawler.controllers.sitemapManager.sitemapModel import SitemapModel


class SitemapController:

    # Private Variables
    __instance = None
    __m_notice_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if SitemapController.__instance is None:
            SitemapController()
        return SitemapController.__instance

    def __init__(self):
        if SitemapController.__instance is not None:
            raise Exception(SitemapModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            SitemapController.__instance = self
            self.__m_notice_model = SitemapModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SitemapModelCommands.M_INIT:
            m_response, m_status = self.__m_notice_model.invoke_trigger(SitemapModelCommands.M_INIT, p_data)
            if m_status is False:
                return render(None, constants.S_TEMPLATE_SITEMAP_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_TEMPLATE_NOTICE_WEBSITE_UPLOAD + "&mNoticeParamData=" + m_response[SitemapCallback.M_SECRETKEY])

