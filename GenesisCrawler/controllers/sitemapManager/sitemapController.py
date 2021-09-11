import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import ErrorMessages
from GenesisCrawler.constants.keys import K_SITEMAP_SECRETKEY
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapModelCommands
from GenesisCrawler.controllers.sitemapManager.sitemapModel import SitemapModel


class SitemapController:

    # Private Variables
    __instance = None
    mNoticeModel = None

    # Initializations
    @staticmethod
    def getInstance():
        if SitemapController.__instance is None:
            SitemapController()
        return SitemapController.__instance

    def __init__(self):
        if SitemapController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            SitemapController.__instance = self
            self.mNoticeModel = SitemapModel()

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == SitemapModelCommands.M_INIT:
            mResponse, mStatus = self.mNoticeModel.invokeTrigger(SitemapModelCommands.M_INIT, pData)
            if mStatus is False:
                return render(None, constants.S_SITEMAP_WEBSITE_PATH, mResponse)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_NOTICE_WEBSITE_UPLOAD_SUCCESS + "&mData=" + mResponse[K_SITEMAP_SECRETKEY])

