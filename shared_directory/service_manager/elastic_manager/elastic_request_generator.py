# Local Imports
import json

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.cms.manage_search.class_model.manage_search_model import manage_search_data_model
from trustly.controllers.view_managers.user.interactive.search_manager.tokenizer import tokenizer
from modules.user_data_parser.parse_services.helper_services.helper_method import helper_method
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.elastic_manager.elastic_enums import ELASTIC_KEYS, ELASTIC_REQUEST_COMMANDS, ELASTIC_INDEX


class elastic_request_generator(request_handler):

    __m_tokenizer = None

    def __init__(self):
        self.__m_tokenizer = tokenizer()

    def __on_search(self, p_query_model):
        m_user_query, m_search_type, m_safe_search, m_page_number = p_query_model.m_search_query, p_query_model.m_search_type, p_query_model.m_safe_search, p_query_model.m_page_number
        m_user_query = m_user_query.lower()
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
            m_image_length_filter = {"range": {"m_img_size": { "gt": 0 }}}

        m_safe_filter = { "match_none": {}}
        m_date_filter = {"range": {"m_date": { "gte": helper_method.get_time() - 30 }}}
        if m_type != "all":
            m_type_filter = {"term": {"m_content_type": m_type[0]}}
        else:
            if m_safe_search == "False":
                m_type_filter = { "match_all": {}}
            else:
                m_type_filter = { "match_all": {}}
                m_safe_filter = {"term": {"m_content_type": 'a'}}

        m_query_statement = {
            "min_score": 1,
            "query": {
                "bool": {
                    "must": [m_image_length_filter, m_date_filter],
                    "should": [
                        {
                            "range": {
                                "date": {
                                    "gte": helper_method.get_time() - 2,
                                    "boost": 3
                                }
                            }
                        },
                        {
                            "range": {
                                "date": {
                                    "gte": helper_method.get_time() - 4,
                                    "boost": 2
                                }
                            }
                        },
                        m_doc_length_filter,
                        {
                            "match": {
                                "m_title": {
                                    "query": m_user_query,
                                    "boost": 2
                                }
                            }
                        },
                        {
                            "match": {
                                "m_meta_description": {
                                    "query": m_user_query,
                                    "boost": 1.5
                                }
                            }
                        },
                        {
                            "match": {
                                "m_important_content": {
                                    "query": m_user_query,
                                    "boost": 1.2
                                }
                            }
                        },
                        {
                            "match": {
                                "m_content": {
                                    "query": m_user_query,
                                    "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            "suggest": {
                "content_suggestion": {
                    "text": m_user_query,
                    "term": {
                        "field": "m_important_content",
                        "min_word_length": 4,
                        "max_term_freq": 0.01,
                        "sort": "score",
                        "string_distance": "internal",
                    }
                }
            },
            "from": (m_page_number - 1) * CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE,
            "size": CONSTANTS.S_SETTINGS_FETCHED_DOCUMENT_SIZE,
        }

        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_WEB_INDEX, ELASTIC_KEYS.S_FILTER:m_query_statement}

    def __onion_list(self, p_page_number):
        m_query = {
            "from": (p_page_number-1) * 5000,
            "size": 5001,
            "query": {
                "match": {
                    "m_sub_host": ''
                }
            },"_source": ["m_host", "m_content_type"]
        }

        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_WEB_INDEX, ELASTIC_KEYS.S_FILTER:m_query}

    def __query_raw(self, p_data:manage_search_data_model):
        m_query = {
            "from": p_data.m_min_range,
            "size": p_data.m_max_range,
            "query": json.loads(json.dumps(json.loads(p_data.m_query)))
            ,"_source": ["m_host", "m_content_type"]
        }
        return {ELASTIC_KEYS.S_DOCUMENT: p_data.m_query_collection, ELASTIC_KEYS.S_FILTER:m_query}


    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_SEARCH:
            return self.__on_search(p_data[0])
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_ONION_LIST:
            return self.__onion_list(p_data[0])
        if p_commands == ELASTIC_REQUEST_COMMANDS.S_QUERY_RAW:
            return self.__query_raw(p_data[0])
