# Local Imports
from genesis.constants.constant import CONSTANTS
from genesis.controllers.data_manager.elastic_manager.elastic_enums import ELASTIC_KEYS, ELASTIC_INDEX, ELASTIC_REQUEST_COMMANDS
from genesis.controllers.search_manager.search_enums import SEARCH_MODEL_TOKENIZATION_COMMANDS
from genesis.controllers.search_manager.tokenizer import tokenizer
from genesis.controllers.shared_model.request_handler import request_handler


class elastic_request_generator(request_handler):

    __m_tokenizer = None

    def __init__(self):
        self.__m_tokenizer = tokenizer()

    def __on_search(self, p_query, p_search_type, p_safe_search, p_page_number):
        m_tokenized_query = self.__m_tokenizer.invoke_trigger(SEARCH_MODEL_TOKENIZATION_COMMANDS.M_TOKENIZE, [p_query])
        m_type = p_search_type

        if m_type == "finance":
            m_type = "business"

        m_doc_length_filter = {"range": {"script.m_doc_size": { "gte": 0 }}}
        if m_type == "doc":
            m_type = "all"
            m_doc_length_filter = {"range": {"script.m_doc_size": { "gt": 0 }}}

        m_image_length_filter = {"range": {"script.m_img_size": { "gte": 0 }}}
        if m_type == "images":
            m_type = "all"
            m_doc_length_filter = {"range": {"script.m_img_size": { "gt": 0 }}}

        m_safe_filter = { "match_none": {}}
        if m_type != "all":
            m_type_filter = {"term": {"script.m_content_type": m_type[0]}}
        else:
            if p_safe_search == "False":
                m_type_filter = { "match_all": {}}
            else:
                m_type_filter = { "match_all": {}}
                m_safe_filter = {"term": {"script.m_content_type": 'a'}}

        print(" ---------------------- ", flush=True)
        print(m_doc_length_filter, flush=True)
        print(" ---------------------- ", flush=True)

        m_query_statement = {
            "from": (p_page_number-1) * CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE,
            "size": CONSTANTS.S_SETTINGS_FETCHED_DOCUMENT_SIZE+5,
            "query": {
                  "bool": {
                  "must_not": [m_safe_filter],
                  "must": [m_type_filter],
                  "should": [
                    m_doc_length_filter,m_image_length_filter,
                    {
                      "match": {
                        "script.m_title": {
                            "query": p_query,
                            "boost": 4
                        }
                      }
                    },
                    {
                      "match": {
                        "script.m_meta_description": {
                            "query": p_query,
                            "boost": 2
                        }
                      }
                    },
                    {
                      "match": {
                        "script.m_important_content": {
                            "query": p_query,
                            "boost": 1
                        }
                      }
                    },
                    {
                      "match": {
                        "script.m_content": {
                            "query": m_tokenized_query,
                            "boost": 0
                        }
                      }
                    }
                  ]
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
                    "script.m_sub_host": 'na'
                }
            },"_source": ["script.m_host", "script.m_content_type"]
        }

        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_WEB_INDEX, ELASTIC_KEYS.S_FILTER:m_query}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_SEARCH:
            return self.__on_search(p_data[0], p_data[1], p_data[2], p_data[3])
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_ONION_LIST:
            return self.__onion_list(p_data[0])
