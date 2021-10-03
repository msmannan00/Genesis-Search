from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelCommands
from GenesisCrawler.controllers.searchManager.SearchModel import SearchModel

class SearchController:

    # Private Variables
    __instance = None
    __m_search_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if SearchController.__instance is None:
            SearchController()
        return SearchController.__instance

    def __init__(self):
        if SearchController.__instance is not None:
            raise Exception(SearchModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            SearchController.__instance = self
            self.__m_search_model = SearchModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SearchModelCommands.M_INIT:
            m_status, m_response = self.__m_search_model.invoke_trigger(SearchModelCommands.M_INIT, p_data)
            if m_status is True:
                return render(None, constants.S_TEMPLATE_SEARCH_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_TEMPLATE_PARENT)
        else:
            m_response = None

        return m_response
