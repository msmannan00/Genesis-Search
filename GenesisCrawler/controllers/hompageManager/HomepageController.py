from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageModelCommands
from GenesisCrawler.controllers.hompageManager.HomepageModel import HomepageModel


class HomepageController:

    # Private Variables
    __instance = None
    __m_homepage_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if HomepageController.__instance is None:
            HomepageController()
        return HomepageController.__instance

    def __init__(self):
        if HomepageController.__instance is not None:
            raise Exception(HomepageModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            HomepageController.__instance = self
            self.__m_homepage_model = HomepageModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command):
        if p_command == HomepageModelCommands.M_INIT:
            m_response, m_status = self.__m_homepage_model.invoke_trigger(HomepageModelCommands.M_INIT, None)
            return render(None, constants.S_TEMPLATE_INDEX_PATH, m_response)
        else:
            m_response = None
        return m_response


'''
    SearchController.getInstance().invokeTrigger(SearchModelCommands.M_INIT, None)
'''
