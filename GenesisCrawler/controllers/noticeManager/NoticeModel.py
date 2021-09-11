from GenesisCrawler.constants import strings
from GenesisCrawler.constants.keys import *
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import *


class NoticeModel:

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass


    def onInitPage(self, pData):

        mContext = {
            K_NOTICE_HEADER: strings.S_GENERAL_EMPTY,
            K_NOTICE_DATA: strings.S_GENERAL_EMPTY,
        }

        if K_NOTICE_PARAM_DATA in pData.GET:
            mContext[K_NOTICE_DATA] = pData.GET[K_NOTICE_PARAM_DATA]

        if K_NOTICE_PARAM_HEADER in pData.GET:
            mContext[K_NOTICE_HEADER] = pData.GET[K_NOTICE_PARAM_HEADER]
            return mContext, True
        else:
            return mContext, False

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == NoticeModelCommands.M_INIT:
            return self.onInitPage(pData)
