# Local Imports
import pymongo
from GenesisCrawler.constants.constant import CONSTANTS
from GenesisCrawler.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_KEYS, MANAGE_USER_MESSAGES, MONGODB_CRUD_COMMANDS
from GenesisCrawler.controllers.data_manager.mongo_manager.mongo_request_generator import mongo_request_generator


class mongo_controller:

    # Local Variables
    __instance = None
    __m_connection = None
    __m_mongo_request_generator = None

    # Initializations
    @staticmethod
    def getInstance():
        if mongo_controller.__instance is None:
            mongo_controller()
        return mongo_controller.__instance

    def __init__(self):
        mongo_controller.__instance = self
        self.__m_mongo_request_generator = mongo_request_generator()
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = pymongo.MongoClient(CONSTANTS.S_MONGO_DATABASE_IP, CONSTANTS.S_MONGO_DATABASE_URL)[CONSTANTS.S_MONGO_DATABASE_NAME]

    def __aggregate(self, p_data):
        try:
            documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].aggregate(p_data[MONGODB_KEYS.S_FILTER])
            return documents
        except Exception as ex:
            return False, str(ex)

    def __replace(self, p_data):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].replace_one(p_data[MONGODB_KEYS.S_FILTER],p_data[MONGODB_KEYS.S_VALUE], True)
            return True, MANAGE_USER_MESSAGES.S_INSERT_SUCCESS
        except Exception as ex:
            return False, str(ex)

    def __create(self, p_data):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].insert(p_data[MONGODB_KEYS.S_VALUE])
            return True, MANAGE_USER_MESSAGES.S_INSERT_SUCCESS
        except Exception as ex:
            return False, str(ex)

    def __read(self, p_data, p_limit):
        try:
            if p_limit is not None:
                documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER]).limit(p_limit)
            else:
                documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER])
            return documents
        except Exception as ex:
            return str(ex)

    def __update(self, p_data, p_upsert):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].update_many(p_data[MONGODB_KEYS.S_FILTER],p_data[MONGODB_KEYS.S_VALUE], upsert=p_upsert)
            return True, MANAGE_USER_MESSAGES.S_UPDATE_SUCCESS

        except Exception as ex:
            return False, str(ex)

    def __delete(self, p_data):
        try:
            documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].remove(p_data[MONGODB_KEYS.S_FILTER])
            return documents, MANAGE_USER_MESSAGES.S_DELETE_SUCCESS
        except Exception as ex:
            return False, str(ex)

    # External Request Callbacks
    def invoke_trigger(self, p_commands, p_data):
        m_request = self.__m_mongo_request_generator.invoke_trigger(p_data[0], p_data[1:])
        if p_commands == MONGODB_CRUD_COMMANDS.S_CREATE:
            return self.__create(m_request)
        elif p_commands == MONGODB_CRUD_COMMANDS.S_READ:
            return self.__read(m_request, p_data[1])
        elif p_commands == MONGODB_CRUD_COMMANDS.S_UPDATE:
            return self.__update(m_request, p_data[1])
        elif p_commands == MONGODB_CRUD_COMMANDS.S_DELETE:
            return self.__delete(m_request)
        elif p_commands == MONGODB_CRUD_COMMANDS.S_REPLACE:
            return self.__replace(m_request)
        elif p_commands == MONGODB_CRUD_COMMANDS.S_AGREGATE:
            return self.__aggregate(m_request)



