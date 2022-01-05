# Local Imports
from elasticsearch import Elasticsearch

from genesis.controllers.service_manager.elastic_manager.elastic_enums import ELASTIC_CONNECTIONS, ELASTIC_INDEX, \
    ELASTIC_CRUD_COMMANDS, ELASTIC_KEYS, MANAGE_ELASTIC_MESSAGES
from genesis.controllers.service_manager.elastic_manager.elastic_request_generator import elastic_request_generator
from genesis.controllers.log_manager.log_controller import log
from genesis.controllers.request_manager.request_handler import request_handler


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
            pass
        except Exception as ex:
            log.g().e("ELASTIC 1 : " + MANAGE_ELASTIC_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))


    def __update(self, p_data, p_upsert):
        try:
            self.__m_connection.index(body=p_data[ELASTIC_KEYS.S_VALUE], index=p_data[ELASTIC_KEYS.S_DOCUMENT])
        except Exception as ex:
            log.g().e("ELASTIC 2 : " + MANAGE_ELASTIC_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))
            return False, str(ex)

    def __read(self, p_data):
        try:
            m_data = self.__m_connection.search(index=p_data[ELASTIC_KEYS.S_DOCUMENT], body=p_data[ELASTIC_KEYS.S_FILTER])
            return self.__m_connection.search(index=p_data[ELASTIC_KEYS.S_DOCUMENT], body=p_data[ELASTIC_KEYS.S_FILTER])

        except Exception as ex:
            log.g().e("ELASTIC 3 : " + MANAGE_ELASTIC_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))
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
