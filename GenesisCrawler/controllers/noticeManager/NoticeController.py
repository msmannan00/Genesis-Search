import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import ErrorMessages
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import NoticeModelCommands
from GenesisCrawler.controllers.noticeManager.NoticeModel import NoticeModel

class NoticeController:

    # Private Variables
    __instance = None
    mNoticeModel = None

    # Initializations
    @staticmethod
    def getInstance():
        if NoticeController.__instance is None:
            NoticeController()
        return NoticeController.__instance

    def __init__(self):
        if NoticeController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            NoticeController.__instance = self
            self.mNoticeModel = NoticeModel()

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == NoticeModelCommands.M_INIT:
            mResponse, mStatus = self.mNoticeModel.invokeTrigger(NoticeModelCommands.M_INIT, pData)
            if mStatus is True:
                return render(None, constants.S_NOTICE_WEBSITE_PATH, mResponse)
            else:
                return HttpResponseRedirect(redirect_to="../")

