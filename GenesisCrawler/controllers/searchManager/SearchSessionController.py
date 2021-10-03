from GenesisCrawler.constants import strings
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchSessionCommands, SearchParam, SearchCallback, SearchDocumentCallback
from GenesisCrawler.controllers.searchManager.searchModel.queryModel import QueryModel
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class SearchSessionController(RequestHandler):

    # Helper Methods
    def __init_search_parameters(self, p_data):
        m_query_model = QueryModel()

        if SearchParam.M_QUERY in p_data.GET:
            m_query_model.set_query(p_data.GET[SearchParam.M_QUERY])
        if SearchParam.M_TYPE in p_data.GET:
            m_query_model.set_search_type(p_data.GET[SearchParam.M_TYPE])
        if SearchParam.M_PAGE in p_data.GET:
            m_query_model.set_page_number(p_data.GET[SearchParam.M_PAGE])
        if SearchParam.M_SAFE_SEARCH in p_data.GET:
            if p_data.GET[SearchParam.M_SAFE_SEARCH] == "True":
                m_query_model.set_safe_search_status("True")
            else:
                m_query_model.set_safe_search_status("False")

        return m_query_model

    def __validate_parameters(self, p_context):
        pass

    def __init_parameters(self, p_document_list, p_search_model):
        mRelevanceContextList = []

        for m_document in p_document_list:
            if p_search_model.get_search_type() != strings.S_SEARCH_CONTENT_TYPE_IMAGE or len(m_document[SearchDocumentCallback.M_IMAGE]) > 0:
                mRelevanceContext = {
                    SearchCallback.M_TITLE: m_document[SearchDocumentCallback.M_TITLE],
                    SearchCallback.M_URL: m_document[SearchDocumentCallback.M_URL],
                    SearchCallback.M_DESCRIPTION: m_document[SearchDocumentCallback.M_DESCRIPTION][0:230] + strings.S_GENERAL_CONTENT_CONTINUE,
                    SearchCallback.K_SEARCH_TYPE: m_document[SearchDocumentCallback.M_CONTENT_TYPE],
                }
                if p_search_model.get_search_type() == strings.S_SEARCH_CONTENT_TYPE_IMAGE:
                    mRelevanceContext[SearchCallback.M_URL] = HelperController.getHost(mRelevanceContext[SearchCallback.M_URL])

                mRelevanceContextList.append(mRelevanceContext)

        if p_search_model.get_page_number()<=3:
            min_range = 1
            max_range = 6
        else:
            min_range = p_search_model.get_page_number() - 2
            max_range = p_search_model.get_page_number() + 3

        m_max_page_reached = False
        if p_search_model.get_total_documents() / constants.S_SETTINGS_SEARCHED_DOCUMENT_SIZE < max_range:
            max_range = int(p_search_model.get_total_documents() / constants.S_SETTINGS_SEARCHED_DOCUMENT_SIZE) + 1

            if p_search_model.get_page_number() >= max_range-1:
                m_max_page_reached = True

        m_status = True
        if p_search_model.get_page_number() > max_range:
            p_search_model.set_page_number(max_range)
            m_max_page_reached = True
            if max_range > 3:
                min_range = max_range-2
            else:
                min_range = 0

        if min_range != max_range:
            m_range = range(min_range,max_range)
        else:
            m_range = None

        mContext = {
            SearchCallback.M_QUERY: p_search_model.get_query(),
            SearchCallback.M_SAFE_SEARCH: p_search_model.get_safe_search_status(),
            SearchCallback.M_CURRENT_PAGE_NUM: p_search_model.get_page_number(),
            SearchCallback.K_SEARCH_TYPE: p_search_model.get_search_type(),
            SearchCallback.M_DOCUMENT: mRelevanceContextList,
            SearchCallback.M_PAGE_NUM: m_range,
            SearchCallback.M_MAX_PAGINATION: m_max_page_reached,
            SearchCallback.M_RESULT_COUNT: strings.S_GENERAL_EMPTY
        }

        if p_search_model.get_total_documents() > constants.S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH:
            mContext[SearchCallback.M_RESULT_COUNT] = HelperController.onCreateRandomSearchCount(p_search_model.get_total_documents())
        else:
            mContext[SearchCallback.M_RESULT_COUNT] = p_search_model.get_total_documents()



        return mContext, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SearchSessionCommands.INIT_SEARCH_PARAMETER:
            return self.__init_search_parameters(p_data[0])
        if p_command == SearchSessionCommands.M_INIT:
            return self.__init_parameters(p_data[0], p_data[1])
        if p_command == SearchSessionCommands.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

