# Local Imports
import hashlib
import json
from datetime import datetime, timedelta

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.cms.manage_search.class_model.manage_search_model import manage_search_data_model
from trustly.controllers.view_managers.user.interactive.search_manager.tokenizer import tokenizer
from app_manager.request_manager.request_handler import request_handler
from app_manager.elastic_manager.elastic_enums import ELASTIC_KEYS, ELASTIC_REQUEST_COMMANDS, ELASTIC_INDEX


class elastic_request_generator(request_handler):
  __m_tokenizer = None

  def __init__(self):
    self.__m_tokenizer = tokenizer()

  def generate_data_hash(self, data):
    data_copy = {key: value for key, value in data.items() if key not in {'m_update_date', 'm_base_url', 'm_url'}}
    data_string = json.dumps(data_copy, sort_keys=True)
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

  def __on_search(self, p_query_model):
    m_user_query, m_search_type, m_safe_search, m_page_number = (
      p_query_model.m_search_query,
      p_query_model.m_search_type,
      p_query_model.m_safe_search,
      p_query_model.m_page_number,
    )
    m_user_query = m_user_query.lower()

    must_not_clause = []
    if m_safe_search == "True":
      must_not_clause.append({"term": {"m_content_type": "toxic"}})

    if m_search_type == "monitor":
      m_query_statement = {
        "min_score": 0,
        "query": {
          "function_score": {
            "query": {
              "bool": {
                "must": [],
                "should": [
                  {
                    "query_string": {
                      "query": m_user_query,
                      "fields": [
                        "m_title^3",
                        "m_meta_description^2",
                        "m_content^1.5",
                        "m_important_content^1.5",
                        "m_content_tokens^2",
                        "m_keywords^1.8"
                      ],
                      "default_operator": "OR",
                      "lenient": True
                    }
                  }
                ],
                "must_not": must_not_clause
              }
            },
            "functions": [
              {
                "gauss": {
                  "m_update_date": {
                    "origin": "now",
                    "scale": "30d",
                    "offset": "10d",
                    "decay": 0.5
                  }
                },
                "weight": 2
              }
            ],
            "boost_mode": "sum"
          }
        },
        "aggs": {
          "limited_base_url": {
            "terms": {
              "field": "m_base_url",
              "size": 100,
              "min_doc_count": 1
            }
          }
        },
        "from": (m_page_number - 1) * CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE_GENERIC,
        "size": CONSTANTS.S_SETTINGS_FETCHED_DOCUMENT_SIZE,
        "track_total_hits": True
      }
      return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_LEAK_INDEX, ELASTIC_KEYS.S_FILTER: m_query_statement}

    else:
      m_query_statement = {
        "min_score": 0,
        "query": {
          "function_score": {
            "query": {
              "bool": {
                "must": [],
                "should": [
                  {
                    "query_string": {
                      "query": m_user_query,
                      "fields": [
                        "m_title^3",
                        "m_meta_description^2",
                        "m_content^1.5",
                        "m_important_content^1.5",
                        "m_content_tokens^2",
                        "m_keywords^1.8"
                      ],
                      "default_operator": "OR",
                      "lenient": True
                    }
                  }
                ],
                "must_not": must_not_clause
              }
            },
            "functions": [
              {
                "gauss": {
                  "m_update_date": {
                    "origin": "now",
                    "scale": "30d",
                    "offset": "10d",
                    "decay": 0.5
                  }
                },
                "weight": 2
              }
            ],
            "boost_mode": "sum"
          }
        },
        "suggest": {
          "important_content_suggestion": {
            "text": m_user_query,
            "term": {
              "field": "m_important_content",
              "min_word_length": 4,
              "max_term_freq": 0.01,
              "sort": "score",
              "string_distance": "internal",
            }
          },
          "content_suggestion": {
            "text": m_user_query,
            "term": {
              "field": "m_content",
              "min_word_length": 4,
              "max_term_freq": 0.01,
              "sort": "score",
              "string_distance": "internal",
            }
          }
        },
        "from": (m_page_number - 1) * CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE_GENERIC,
        "size": CONSTANTS.S_SETTINGS_FETCHED_DOCUMENT_SIZE,
        "track_total_hits": True
      }
      return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_GENERIC_INDEX, ELASTIC_KEYS.S_FILTER: m_query_statement}

  def __onion_list(self, p_page_number):
    m_query = {
      "from": (p_page_number - 1) * 5000,
      "size": 5001,
      "query": {
        "match": {
          "m_sub_host": ''
        }
      }, "_source": ["m_host", "m_content_type"]
    }

    return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_GENERIC_INDEX, ELASTIC_KEYS.S_FILTER: m_query}

  def __query_raw(self, p_data: manage_search_data_model):
    m_query = {
      "from": p_data.m_min_range,
      "size": p_data.m_max_range,
      "query": json.loads(json.dumps(json.loads(p_data.m_query)))
      , "_source": ["m_host", "m_content_type"]
    }
    return {ELASTIC_KEYS.S_DOCUMENT: p_data.m_query_collection, ELASTIC_KEYS.S_FILTER: m_query}

  def __clear_expire_index(self):
    threshold_time = datetime.utcnow() - timedelta(seconds=CONSTANTS.S_SETTINGS_INDEX_EXPIRY)
    return  {
      "query": {
        "range": {
          "m_update_date": {
            "lt": threshold_time.isoformat()
          }
        }
      }
    }

  def __index_query_general(self, p_index_data, p_index_name):
    index_entries = []
    current_timestamp = datetime.utcnow().isoformat()

    if isinstance(p_index_data, list):
      pass
    else:
      p_index_data['m_update_date'] = current_timestamp
      p_index_data['m_hash_content'] = hashlib.sha256((p_index_data['m_important_content'] + p_index_data['m_title']).encode()).hexdigest()
      p_index_data['m_hash_url'] = hashlib.sha256((p_index_data['m_url'] + p_index_data['m_title']).encode()).hexdigest()
      p_index_data['m_hash'] = p_index_data['m_url']

      index_entries.append({
        ELASTIC_KEYS.S_DOCUMENT: p_index_name,
        ELASTIC_KEYS.S_VALUE: p_index_data
      })

    return index_entries

  def __index_query_leak(self, p_index_data, p_index_name):
    contact_link = p_index_data.get("contact_link", "")
    index_entries = []
    current_timestamp = datetime.utcnow().isoformat()

    for card in p_index_data.get("cards_data", []):
      data_hash = self.generate_data_hash(card)
      entry = {
        "m_title": card.get("m_title", ""),
        "m_url": card.get("m_url", ""),
        "m_base_url": card.get("m_base_url", ""),
        "m_content": card.get("m_content", ""),
        "m_important_content": card.get("m_important_content", ""),
        "m_weblink": card.get("m_weblink", ""),
        "m_dumplink": card.get("m_dumplink", ""),
        "m_content_type": card.get("m_content_type", ""),
        "m_extra_tags": card.get("m_extra_tags", []),
        "m_contact_link": contact_link,
        "m_update_date": current_timestamp,
        "m_hash": data_hash
      }
      index_entries.append({
        ELASTIC_KEYS.S_DOCUMENT: p_index_name,
        ELASTIC_KEYS.S_VALUE: entry
      })

    return index_entries

  def invoke_trigger(self, p_commands, p_data=None):
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_SEARCH:
      return self.__on_search(p_data[0])
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_ONION_LIST:
      return self.__onion_list(p_data[0])
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_QUERY_RAW:
      return self.__query_raw(p_data[0])
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_CLEAR_EXPIRE_INDEX:
      return self.__clear_expire_index()
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_INDEX_GENERAL:
      return self.__index_query_general(p_data[0], p_data[1])
    if p_commands == ELASTIC_REQUEST_COMMANDS.S_INDEX_LEAK:
      return self.__index_query_leak(p_data[0], p_data[1])
