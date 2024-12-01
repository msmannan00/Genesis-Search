from trustly.controllers.helper_manager.env_handler import env_handler


class REDIS_CONNECTIONS:
  S_DATABASE_IP = 'redis_server'
  S_DATABASE_PORT = 6379
  S_DATABASE_PASSWORD = env_handler.get_instance().env('REDIS_PASSWORD')


class REDIS_KEYS:
  INSIGHT_OLD = "INSIGHT_OLD"
  INSIGHT_NEW = "INSIGHT_NEW"
  INSIGHT_STAT = "INSIGHT_STAT"

class REDIS_DEFAULT:
  INSIGHT_DEFAULT = "{'generic_model': [{'Doc Count': 0}, {'Unique_Base_URLs': 0}, {'URL / Doc': 0}, {'Archive / Doc': 0}, {'Email / Doc': 0}, {'Phone / Doc': 0}, {'Average Score': 0}, {'Common Type': 'general'}, {'Updated 5 Days': 0}, {'Updated 9 Days': 0}, {'Most Recent': '01 Dec'}, {'Oldest Update': '01 Dec'}], 'leak_model': [{'Doc Count': 0}, {'Unique_Base_URLs': 0}, {'Dumps / Doc': 0}, {'URL / Doc': 0}, {'Updated 5 Days': 0}, {'Updated 9 Days': 0}, {'Most Recent': '01 Dec'}, {'Oldest Update': '01 Dec'}]}"

class REDIS_COMMANDS:
  S_SET_BOOL = 1
  S_GET_BOOL = 2
  S_SET_INT = 3
  S_GET_INT = 4
  S_SET_STRING = 5
  S_GET_STRING = 6
  S_SET_LIST = 7
  S_GET_LIST = 8
  S_GET_KEYS = 9
  S_GET_FLOAT = 10
  S_SET_FLOAT = 11
  S_FLUSH_ALL = 12
  S_ACQUIRE_LOCK = 13
  S_RELEASE_LOCK = 14
