from bson import ObjectId

from genesis.constants.constant import CONSTANTS
from genesis.constants.enums import MONGO_COMMANDS, TFIDF_COMMANDS
from genesis.constants.strings import GENERAL_STRINGS, SEARCH_STRINGS
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_CRUD_COMMANDS
from genesis.controllers.data_manager.tfidf_manager.tfidf_controller import tfidf_controller
from genesis.controllers.search_manager.search_enums import SEARCH_MODEL_COMMANDS, SEARCH_MODEL_SPELL_CHECKER, SEARCH_MODEL_TOKENIZATION_COMMANDS, SEARCH_CALLBACK, SEARCH_SESSION_COMMANDS
from genesis.controllers.search_manager.search_session_controller import search_session_controller
from genesis.controllers.search_manager.spell_checker import spell_checker
from genesis.controllers.search_manager.tokenizer import tokenizer
from genesis.controllers.shared_model.request_handler import request_handler


class search_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None
    __m_tokenizer = None
    __m_spell_checker = None

    # Initializations
    def __init__(self):
        self.__m_session = search_session_controller()
        self.__m_tokenizer = tokenizer()
        self.__m_spell_checker = spell_checker()

    def __paged_documents(self, m_documents, p_query_model):

        if p_query_model.m_search_type != SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:
            m_size = CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE
        else:
            m_size = CONSTANTS.S_SETTINGS_SEARCHED_IMAGE_SIZE

        if p_query_model.m_page_number > len(m_documents) / m_size:
            p_query_model.set_page_number(len(m_documents) / m_size)

        if p_query_model.m_page_number == 1:
            m_best_list = m_documents[int(p_query_model.m_page_number)*m_size:int(p_query_model.m_page_number) * m_size + m_size + 20]
        else:
            m_best_list = m_documents[int(p_query_model.m_page_number) * m_size:int(p_query_model.m_page_number) * m_size + m_size]
        return m_best_list

    def __fetch_filtered_documents(self, p_paged_documents):
        mRelevanceListData = []
        try:
            for m_service in p_paged_documents:
                m_result = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_READ, [MONGO_COMMANDS.M_FETCH_DOCUMENT_BY_ID, None, m_service.m_document_id])
                mRelevanceListData.append(m_result.next())
            return mRelevanceListData
        except Exception as ex:
            return mRelevanceListData


    def __query_results(self, p_data):
        m_query_model = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER, [p_data])
        if m_query_model.m_search_query == GENERAL_STRINGS.S_GENERAL_EMPTY:
            return False, None
        # m_query_model = p_data

        m_tokenized_query = self.__m_tokenizer.invoke_trigger(SEARCH_MODEL_TOKENIZATION_COMMANDS.M_TOKENIZE, [m_query_model.m_search_query])
        m_tokenized_query_non_indexed = tfidf_controller.getInstance().invoke_trigger(TFIDF_COMMANDS.M_GET_NON_INDEXED_TOKENS, [m_tokenized_query])
        m_document_cursor = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_AGREGATE, [MONGO_COMMANDS.M_SEARCH_BY_TOKEN, m_tokenized_query_non_indexed, m_query_model])
        m_documents = tfidf_controller.getInstance().invoke_trigger(TFIDF_COMMANDS.M_POPULATE_SEARCH, [m_tokenized_query, m_document_cursor])
        m_query_model.set_total_documents(len(m_documents))

        m_paged_documents = self.__paged_documents(m_documents, m_query_model)

        m_filtered_documents = self.__fetch_filtered_documents(m_paged_documents)
        m_context, m_status = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.M_INIT, [m_filtered_documents, m_query_model])
        m_context[SEARCH_CALLBACK.M_QUERY_ERROR] = self.__m_spell_checker.invoke_trigger(SEARCH_MODEL_SPELL_CHECKER.M_CHECK_SPELLING, [m_tokenized_query_non_indexed])
        return m_status, m_context

    def __init_page(self, p_data):
        mStatus, mResult = self.__query_results(p_data)
        return mStatus, mResult

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
