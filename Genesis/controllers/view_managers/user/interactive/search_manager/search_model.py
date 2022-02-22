import json

from Genesis.controllers.constants.strings import GENERAL_STRINGS
from Genesis.controllers.view_managers.user.interactive.search_manager.search_enums import SEARCH_CALLBACK, SEARCH_MODEL_TOKENIZATION_COMMANDS, SEARCH_SESSION_COMMANDS, SEARCH_MODEL_COMMANDS
from Genesis.controllers.view_managers.user.interactive.search_manager.search_session_controller import search_session_controller
from Genesis.controllers.view_managers.user.interactive.search_manager.spell_checker import spell_checker
from Genesis.controllers.view_managers.user.interactive.search_manager.tokenizer import tokenizer
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.elastic_manager.elastic_controller import elastic_controller
from shared_directory.service_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS


class search_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None
    __m_spell_checker = None
    __m_tokenizer = None

    # Initializations
    def __init__(self):
        self.__m_session = search_session_controller()
        self.__m_tokenizer = tokenizer()
        self.__m_spell_checker = spell_checker()

    def __parse_filtered_documents(self, p_paged_documents):
        mRelevanceListData = []
        try:
            m_result_final = p_paged_documents['hits']['hits']

            for m_document in m_result_final:
                m_service = m_document['_source']
                if m_service['m_sub_host'] == "na":
                    m_service['m_sub_host'] = "/"
                mRelevanceListData.append(m_document['_source'])

            return mRelevanceListData, p_paged_documents['suggest']['content_suggestion']
        except Exception as ex:
            return mRelevanceListData, []

    def __query_results(self, p_data):
        m_query_model = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER, [p_data])
        if m_query_model.m_search_query == GENERAL_STRINGS.S_GENERAL_EMPTY:
           return False, None

        m_tokenized_query = self.__m_tokenizer.invoke_trigger(SEARCH_MODEL_TOKENIZATION_COMMANDS.M_SPLIT_AND_NORMALIZE, [m_query_model.m_search_query])
        m_status, m_documents = elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.S_SEARCH,[m_query_model],[None]])

        print("--------",flush=True)
        print(json.dumps(m_documents),flush=True)
        print("--------",flush=True)

        m_parsed_documents, m_suggestions_content = self.__parse_filtered_documents(m_documents)
        m_query_model.set_total_documents(len(m_parsed_documents))

        m_context, m_status = self.__m_session.invoke_trigger(SEARCH_SESSION_COMMANDS.M_INIT, [m_parsed_documents, m_query_model, m_tokenized_query])
        m_context[SEARCH_CALLBACK.M_QUERY_ERROR_URL], m_context[SEARCH_CALLBACK.M_QUERY_ERROR] = self.__m_spell_checker.generate_suggestions(m_query_model.m_search_query, m_suggestions_content)

        return m_status, m_context

    def __init_page(self, p_data):
        mStatus, mResult = self.__query_results(p_data)
        return mStatus, mResult

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
