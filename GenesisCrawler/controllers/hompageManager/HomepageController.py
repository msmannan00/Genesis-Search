from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import ErrorMessages, MongoDBCommands
from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageModelCommands
from GenesisCrawler.controllers.hompageManager.HomepageModel import HomepageModel
from GenesisCrawler.controllers.mongoDBManager.mongoDBController import mongoDBController


class HomepageController:

    # Private Variables
    __instance = None
    mHomePageModel = None

    # Initializations
    @staticmethod
    def getInstance():
        if HomepageController.__instance is None:
            HomepageController()
        return HomepageController.__instance

    def __init__(self):
        if HomepageController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            HomepageController.__instance = self
            self.mHomePageModel = HomepageModel()

    # External Request Callbacks
    def invokeTrigger(self, pCommand):
        if pCommand == HomepageModelCommands.M_INIT:
            m_response = self.mHomePageModel.invokeTrigger(HomepageModelCommands.M_INIT, None)
            return render(None, constants.S_INDEX_PATH, m_response)
        else:
            m_response = None
        return m_response

mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_SEARCH, "SEX")