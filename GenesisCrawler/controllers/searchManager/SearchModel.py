
from GenesisCrawler.constants import strings
from GenesisCrawler.constants.constant import constants
from GenesisCrawler.constants.enums import MongoDBCommands, TFIDFCommands
from GenesisCrawler.controllers.dataManager.TfIdfManager.TfIdfController import TfIdfController
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelCommands, SearchModelSpellCheckerCommands, SearchModelTokenizerCommands, SearchCallback, SearchSessionCommands
from GenesisCrawler.controllers.searchManager.SearchSessionController import SearchSessionController
from GenesisCrawler.controllers.searchManager.SpellChecker import SpellChecker
from GenesisCrawler.controllers.searchManager.Tokenizer import Tokenizer
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class SearchModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None
    __m_tokenizer = None
    __m_spell_checker = None

    # Initializations
    def __init__(self):
        self.__m_session = SearchSessionController()
        self.__m_tokenizer = Tokenizer()
        self.__m_spell_checker = SpellChecker()

    def __paged_documents(self, m_documents, p_query_model):

        if p_query_model.get_search_type() != strings.S_SEARCH_CONTENT_TYPE_IMAGE:
            m_size = constants.S_SETTINGS_SEARCHED_DOCUMENT_SIZE
        else:
            m_size = constants.S_SETTINGS_SEARCHED_IMAGE_SIZE

        if p_query_model.get_page_number() > len(m_documents) / m_size:
            p_query_model.set_page_number(len(m_documents) / m_size)

        if p_query_model.get_page_number() == 1:
            m_best_list = m_documents[int(p_query_model.get_page_number())*m_size:int(p_query_model.get_page_number()) * m_size + m_size + 20]
        else:
            m_best_list = m_documents[int(p_query_model.get_page_number()) * m_size:int(p_query_model.get_page_number()) * m_size + m_size]
        return m_best_list

    def __query_results(self, p_data):
        m_query_model = self.__m_session.invoke_trigger(SearchSessionCommands.INIT_SEARCH_PARAMETER, [p_data])
        if m_query_model.get_query() == strings.S_GENERAL_EMPTY:
            return False, None

        m_tokenized_query = self.__m_tokenizer.invoke_trigger(SearchModelTokenizerCommands.M_TOKENIZE, [m_query_model.get_query()])
        m_tokenized_query_non_indexed = TfIdfController.getInstance().invoke_trigger(TFIDFCommands.M_GET_NON_INDEXED_TOKENS, [m_tokenized_query])
        m_document_cursor = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_SEARCH, [m_tokenized_query_non_indexed, m_query_model])
        m_documents = TfIdfController.getInstance().invoke_trigger(TFIDFCommands.M_POPULATE_SEARCH, [m_tokenized_query, m_document_cursor])
        m_query_model.set_total_documents(len(m_documents))
        m_paged_documents = self.__paged_documents(m_documents, m_query_model)
        m_filtered_documents = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_FETCH_DOCUMENTS, [m_paged_documents, m_query_model.get_search_type()])
        m_context, m_status = self.__m_session.invoke_trigger(SearchSessionCommands.M_INIT, [m_filtered_documents, m_query_model])
        m_context[SearchCallback.M_QUERY_ERROR] = self.__m_spell_checker.invoke_trigger(SearchModelSpellCheckerCommands.M_CHECK_SPELLING, [m_tokenized_query_non_indexed])
        return m_status, m_context

    def __init_page(self, p_data):
        mStatus, mResult = self.__query_results(p_data)
        return mStatus, mResult

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SearchModelCommands.M_INIT:
            return self.__init_page(p_data)
