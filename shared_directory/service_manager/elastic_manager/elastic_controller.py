# Local Imports
from elasticsearch import Elasticsearch

from shared_directory.log_manager.log_controller import log
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.elastic_manager.elastic_enums import ELASTIC_CONNECTIONS, ELASTIC_INDEX, \
    MANAGE_ELASTIC_MESSAGES, ELASTIC_KEYS, ELASTIC_CRUD_COMMANDS
from shared_directory.service_manager.elastic_manager.elastic_request_generator import elastic_request_generator


class elastic_controller(request_handler):
    __instance = None
    __m_connection = None
    __m_elastic_request_generator = None

    # Initializations
    @staticmethod
    def get_instance():
        if elastic_controller.__instance is None:
            elastic_controller()
        return elastic_controller.__instance

    def __init__(self):
        elastic_controller.__instance = self
        self.__m_elastic_request_generator = elastic_request_generator()
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = Elasticsearch(ELASTIC_CONNECTIONS.S_DATABASE_IP + ":" + str(ELASTIC_CONNECTIONS.S_DATABASE_PORT))
        self.__initialization()

    def __initialization(self):
        try:
            #####  VERY DANGEROUS DO IT VERY CAREFULLY  #####
            # self.__m_connection.indices.delete(index=ELASTIC_INDEX.S_WEB_INDEX, ignore=[400, 404])
            if self.__m_connection.indices.exists(index=ELASTIC_INDEX.S_WEB_INDEX) is False:
                m_mapping = {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "max_result_window" : 1000000
                    },
                    "mappings": {
                        "_source": {
                            "enabled": True
                        },

                        "dynamic":"strict" ,
                        "properties": {
                            'm_host': { 'type': 'keyword' },
                            'm_sub_host': { 'type': 'keyword' },
                            "m_doc_size": { 'type': 'integer', },
                            "m_img_size": {'type': 'integer'},
                            'm_title': {'type': 'text'},
                            'm_title_hidden': {'type': 'text'},
                            'm_meta_description': {'type': 'text'},
                            'm_important_content': {'type': 'text'},
                            'm_important_content_hidden': {'type': 'text'},
                            'm_meta_keywords': {'type': 'text'},
                            'm_content': {'type': 'text'},
                            'm_user_generated': {'type': 'boolean'},
                            'm_content_type': {'type': 'keyword'},
                            "m_images": { "type": "nested",
                                    "properties": {
                                    "m_url": {
                                        "type": "keyword"
                                    },
                                    "m"
                                    "_type": {
                                        "type": "keyword"
                                    }
                                }
                            },
                            'm_crawled_user_images': { "type" : "text" },
                            'm_crawled_doc_url': { "type" : "text" },
                            'm_crawled_video': { "type" : "text" },
                            'm_doc_url': { "type" : "text" },
                            'm_video': { "type" : "text" },
                            'm_daily_hits': {'type': 'integer'},
                            'm_half_month_hits': {'type': 'integer'},
                            'm_date': {'type': 'integer'},
                            'm_monthly_hits': {'type': 'integer'},
                            'm_total_hits': {'type': 'integer'}
                        }
                    }
                }
                self.__m_connection.indices.create(
                    index=ELASTIC_INDEX.S_WEB_INDEX,
                    body=m_mapping
                )

        except Exception as ex:
            log.g().e("ELASTIC 1 : " + MANAGE_ELASTIC_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))


    def __update(self, p_data, p_upsert):
        try:
            self.__m_connection.update(body=p_data[ELASTIC_KEYS.S_VALUE],id=p_data[ELASTIC_KEYS.S_ID], index=p_data[ELASTIC_KEYS.S_DOCUMENT])
            return True, None
        except Exception as ex:
            log.g().e("ELASTIC 2 : " + MANAGE_ELASTIC_MESSAGES.S_UPDATE_FAILURE + " : " + str(ex))
            return False, str(ex)

    def __read(self, p_data):
        try:
            return True, self.__m_connection.search(index=p_data[ELASTIC_KEYS.S_DOCUMENT], body=p_data[ELASTIC_KEYS.S_FILTER])

        except Exception as ex:
            log.g().e("ELASTIC 3 : " + MANAGE_ELASTIC_MESSAGES.S_READ_FAILURE + " : " + str(ex))
            return False, str(ex)

    def __index(self, p_data):
        try:
            self.__m_connection.index(body=p_data[ELASTIC_KEYS.S_VALUE],id=p_data[ELASTIC_KEYS.S_ID], index=p_data[ELASTIC_KEYS.S_DOCUMENT])
            return True, None
        except Exception as ex:
            log.g().e(MANAGE_ELASTIC_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))
            return False, str(ex)

    def invoke_trigger(self, p_commands, p_data=None):

        m_request = p_data[0]
        m_data = p_data[1]
        m_param = p_data[2]

        m_request = self.__m_elastic_request_generator.invoke_trigger(m_request, m_data)
        if p_commands == ELASTIC_CRUD_COMMANDS.S_UPDATE:
            return self.__update(m_request, m_param[0])
        if p_commands == ELASTIC_CRUD_COMMANDS.S_READ:
            return self.__read(m_request)
        if p_commands == ELASTIC_CRUD_COMMANDS.S_INDEX:
            return self.__index(m_request)
