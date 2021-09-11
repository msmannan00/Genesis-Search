
from GenesisCrawler.constants import strings
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.keys import *
from GenesisCrawler.constants.message import *
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.mongoDBManager.mongoDBController import mongoDBController
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportModelCommands


class ReportModel:

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass

    def validateParameters(self, pData, pContext):
        mValidityStatus = True

        if pContext[K_REPORT_URL] == strings.S_GENERAL_EMPTY:
            pContext[K_REPORT_URL_ERROR] = S_REPORT_URL_INCOMPLETE_ERROR
            mValidityStatus = False
        elif pContext[K_REPORT_URL].startswith("http") is False:
            pContext[K_REPORT_URL_ERROR] = S_REPORT_URL_INVALID_PROTOCOL
            mValidityStatus = False
        elif HelperController.isURLValid(pContext[K_REPORT_URL]) is False:
            pContext[K_REPORT_URL_ERROR] = S_REPORT_URL_INVALID_ERROR
            mValidityStatus = False

        if pContext[K_REPORT_EMAIL] != strings.S_GENERAL_EMPTY and HelperController.isMailValid(pContext[K_REPORT_EMAIL]) is False:
            pContext[K_REPORT_EMAIL_ERROR] = S_REPORT_URL_INVALID_EMAIL
            mValidityStatus = False

        return pContext, mValidityStatus

    def initParameters(self, pData):
        mContext = {
            K_REPORT_URL: strings.S_GENERAL_EMPTY,
            K_REPORT_EMAIL: strings.S_GENERAL_EMPTY,
            K_REPORT_MESSAGE: strings.S_GENERAL_EMPTY,
            K_REPORT_URL_ERROR: strings.S_GENERAL_EMPTY,
            K_REPORT_EMAIL_ERROR: strings.S_GENERAL_EMPTY,
        }

        if K_REPORT_PARAM_URL in pData.POST:
            mContext[K_REPORT_URL] = pData.POST[K_REPORT_PARAM_URL]
        else:
            return mContext, False

        if K_REPORT_PARAM_EMAIL in pData.POST:
            mContext[K_REPORT_EMAIL] = pData.POST[K_REPORT_PARAM_EMAIL]
        if K_REPORT_PARAM_MESSAGE in pData.POST:
            mContext[K_REPORT_MESSAGE] = pData.POST[K_REPORT_PARAM_MESSAGE]

        return mContext, True

    def uploadWebsite(self, pContext):
        mData = {
            K_MONGO_REPORT_URL: pContext[K_REPORT_URL],
            K_MONGO_REPORT_EMAIL: pContext[K_REPORT_EMAIL],
            K_MONGO_REPORT_MESSAGE: pContext[K_REPORT_MESSAGE],
        }

        mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_REPORT_URL, mData)

    def onInitPage(self, pData):

        mContext, mStatus = self.initParameters(pData)
        if mStatus is False:
            return mContext, False

        mContext, mStatus = self.validateParameters(pData, mContext)
        if mStatus is True and '.onion' in HelperController.getHost(mContext[K_REPORT_URL]):
            self.uploadWebsite(mContext)
            mContext = {}

        return mContext, mStatus

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == ReportModelCommands.M_INIT:
            return self.onInitPage(pData)
