# Local Imports
import pymongo

from app_manager.log_manager.log_controller import log
from app_manager.mongo_manager.mongo_enums import MONGO_CONNECTIONS, MONGODB_COLLECTIONS, MONGODB_KEYS, MANAGE_MONGO_MESSAGES, MONGODB_CRUD, MONGO_USER_COLLECTION
from app_manager.mongo_manager.mongo_request_generator import mongo_request_generator


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
    self.__m_connection = pymongo.MongoClient(MONGO_CONNECTIONS.S_MONGO_DATABASE_IP, MONGO_CONNECTIONS.S_MONGO_DATABASE_PORT, username=MONGO_CONNECTIONS.S_MONGO_USERNAME, password=MONGO_CONNECTIONS.S_MONGO_PASSWORD)[MONGO_CONNECTIONS.S_MONGO_DATABASE_NAME]
    self.__initialize_database()

  def __initialize_database(self):
    try:
      if MONGODB_COLLECTIONS.S_USER_MODEL not in self.__m_connection.list_collection_names():
        m_user = self.__m_connection.create_collection(name=MONGODB_COLLECTIONS.S_USER_MODEL)
        m_user.insert_one(MONGO_USER_COLLECTION.S_DATABASE_DEFAULT_ENTRY_USER)

      if MONGODB_COLLECTIONS.S_STATUS not in self.__m_connection.list_collection_names():
        m_status = self.__m_connection.get_collection(name=MONGODB_COLLECTIONS.S_STATUS)
        m_status.insert_one(MONGO_USER_COLLECTION.S_DATABASE_DEFAULT_ENTRY_STATUS)

    except Exception as ex:
      print(ex)
      pass

  def __create(self, p_data):
    try:
      self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].insert_one(p_data[MONGODB_KEYS.S_VALUE])
      return True, MANAGE_MONGO_MESSAGES.S_INSERT_SUCCESS
    except Exception as ex:
      log.g().e("MONGO E2 : " + MANAGE_MONGO_MESSAGES.S_INSERT_FAILURE + " : " + str(ex))
      return False, str(ex)

  def __read(self, p_data, p_skip, p_limit):
    try:
      if p_limit is not None:
        documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER]).skip(p_skip).limit(p_limit)
      else:
        documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER])
      return documents, True
    except Exception as ex:
      log.g().e("MONGO E3 : " + MANAGE_MONGO_MESSAGES.S_READ_FAILURE + " : " + str(ex))
      return str(ex), False

  def __replace(self, p_data, p_upsert):
    try:
      self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].replace_one(p_data[MONGODB_KEYS.S_FILTER], p_data[MONGODB_KEYS.S_VALUE], upsert=p_upsert)
      return True, MANAGE_MONGO_MESSAGES.S_REPLACE_SUCCESS

    except Exception as ex:
      log.g().e("MONGO E4 : " + MANAGE_MONGO_MESSAGES.S_REPLACE_FAILURE + " : " + str(ex))
      return False, str(ex)

  def __update(self, p_data):
    try:
      self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].update_one(p_data[MONGODB_KEYS.S_FILTER], p_data[MONGODB_KEYS.S_VALUE], upsert=False)
      return True, MANAGE_MONGO_MESSAGES.S_UPDATE_SUCCESS

    except Exception as ex:
      log.g().e("MONGO E4 : " + MANAGE_MONGO_MESSAGES.S_UPDATE_FAILURE + " : " + str(ex))
      return False, str(ex)

  def __delete(self, p_data):
    try:
      documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].remove(p_data[MONGODB_KEYS.S_FILTER])
      return documents, MANAGE_MONGO_MESSAGES.S_DELETE_SUCCESS
    except Exception as ex:
      log.g().e("MONGO E5 : " + MANAGE_MONGO_MESSAGES.S_DELETE_FAILURE + " : " + str(ex))
      return False, str(ex)

  def invoke_trigger(self, p_commands, p_data=None):
    pass

    m_request = p_data[0]
    m_data = p_data[1]
    m_param = p_data[2]

    m_request = self.__m_mongo_request_generator.invoke_trigger(m_request, m_data)

    if p_commands == MONGODB_CRUD.S_CREATE:
      return self.__create(m_request)
    elif p_commands == MONGODB_CRUD.S_READ:
      return self.__read(m_request, m_param[0], m_param[1])
    elif p_commands == MONGODB_CRUD.S_UPDATE:
      return self.__update(m_request)
    elif p_commands == MONGODB_CRUD.S_REPLACE:
      return self.__replace(m_request, m_param[0])
    elif p_commands == MONGODB_CRUD.S_DELETE:
      return self.__delete(m_request)
