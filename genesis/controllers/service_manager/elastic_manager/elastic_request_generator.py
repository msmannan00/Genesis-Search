# Local Imports
from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.service_manager.elastic_manager.elastic_enums import ELASTIC_INDEX, ELASTIC_KEYS, ELASTIC_REQUEST_COMMANDS
from genesis.controllers.view_managers.search_manager.search_enums import SEARCH_MODEL_TOKENIZATION_COMMANDS
from genesis.controllers.view_managers.search_manager.tokenizer import tokenizer


class elastic_request_generator(request_handler):

    __m_tokenizer = None

    def __init__(self):
        self.__m_tokenizer = tokenizer()

    def __on_search(self, p_query_model, p_suggested_query):
        m_user_query, m_search_type, m_safe_search, m_page_number = p_query_model.m_search_query, p_query_model.m_search_type, p_query_model.m_safe_search, p_query_model.m_page_number

        m_tokenized_query = self.__m_tokenizer.invoke_trigger(SEARCH_MODEL_TOKENIZATION_COMMANDS.M_NORMALIZE, [m_user_query])
        m_type = m_search_type

        if m_type == "finance":
            m_type = "business"

        m_doc_length_filter = {"range": {"m_doc_size": { "gte": 0 }}}
        if m_type == "doc":
            m_type = "all"
            m_doc_length_filter = {"range": {"m_doc_size": { "gt": 0 }}}

        m_image_length_filter = {"range": {"m_img_size": { "gte": 0 }}}
        if m_type == "images":
            m_type = "all"
            m_doc_length_filter = {"range": {"m_img_size": { "gt": 0 }}}

        m_safe_filter = { "match_none": {}}
        if m_type != "all":
            m_type_filter = {"term": {"m_content_type": m_type[0]}}
        else:
            if m_safe_search == "False":
                m_type_filter = { "match_all": {}}
            else:
                m_type_filter = { "match_all": {}}
                m_safe_filter = {"term": {"m_content_type": 'a'}}

        m_query_statement = {
            "from": (m_page_number-1) * CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE,
            "size": CONSTANTS.S_SETTINGS_FETCHED_DOCUMENT_SIZE+5,
            "query": {
                  "bool": {
                  "must_not": [m_safe_filter],
                  "must": [m_type_filter],
                  "should": [
                    m_doc_length_filter,m_image_length_filter,
                    {
                      "match": {
                        "m_title": {
                            "query": m_user_query,
                            "boost": 4
                        }
                      }
                    },
                    {
                      "match": {
                        "m_meta_description": {
                            "query": m_user_query,
                            "boost": 2
                        }
                      }
                    },
                    {
                      "match": {
                        "m_important_content": {
                            "query": m_user_query,
                            "boost": 1
                        }
                      }
                    },
                    {
                      "match": {
                        "m_content": {
                            "query": m_tokenized_query,
                            "boost": 0
                        }
                      }
                    }
                  ]
                }
            },
              "suggest" : {
                "suggestions" : {
                  "text" : p_suggested_query,
                  "term" : {
                    "field" : "m_content"
                  }
               }
            }
         }

        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_WEB_INDEX, ELASTIC_KEYS.S_FILTER:m_query_statement}

    def __onion_list(self, p_page_number):
        m_query = {
            "from": (p_page_number-1) * 5000,
            "size": 5001,
            "query": {
                "match": {
                    "m_sub_host": 'na'
                }
            },"_source": ["m_host", "m_content_type"]
        }

        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_WEB_INDEX, ELASTIC_KEYS.S_FILTER:m_query}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_SEARCH:
            return self.__on_search(p_data[0], p_data[1])
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_ONION_LIST:
            return self.__onion_list(p_data[0])
