
from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import ErrorMessages
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelCommands
from GenesisCrawler.controllers.searchManager.SearchModel import SearchModel


class SearchController:

    # Private Variables
    __instance = None
    mSearchModel = None

    # Initializations
    @staticmethod
    def getInstance():
        if SearchController.__instance is None:
            SearchController()
        return SearchController.__instance

    def __init__(self):
        if SearchController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            SearchController.__instance = self
            self.mSearchModel = SearchModel()

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == SearchModelCommands.M_INIT:
            mStatus, m_response = self.mSearchModel.invokeTrigger(SearchModelCommands.M_INIT, pData)
            if mStatus is True:
                return render(None, constants.S_SEARCH_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to=constants.S_NOTICE_WEBSITE_REPORT_SUCCESS)
        else:
            m_response = None

        return m_response

