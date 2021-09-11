from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.keys import *
from GenesisCrawler.controllers.mongoDBManager.mongoDBController import mongoDBController
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelCommands


class SearchModel:

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass

    def onRecieveSearchResults(self, pData):
        return True, mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_SEARCH, pData.GET[K_SITEMAP_PARAM_SEARCH])

    def onInitPage(self, pData):
        mStatus, mResult = self.onRecieveSearchResults(pData)
        return mStatus, mResult

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == SearchModelCommands.M_INIT:
            return self.onInitPage(pData)
