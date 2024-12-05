from trustly.controllers.helper_manager.env_handler import env_handler


class REDIS_CONNECTIONS:
  S_DATABASE_IP = 'redis_server'
  S_DATABASE_PORT = 6379
  S_DATABASE_PASSWORD = env_handler.get_instance().env('REDIS_PASSWORD')


class REDIS_KEYS:
  INSIGHT_OLD_DAY = "INSIGHT_OLD_DAY"
  INSIGHT_NEW_DAY = "INSIGHT_NEW_DAY"
  INSIGHT_STAT_DAY = "INSIGHT_STAT_DAY"
  INSIGHT_OLD_WEEK = "INSIGHT_OLD_WEEK"
  INSIGHT_NEW_WEEK = "INSIGHT_NEW_WEEK"
  INSIGHT_STAT_WEEK = "INSIGHT_STAT_WEEK"

class REDIS_DEFAULT:
  INSIGHT_DEFAULT = "{'generic_model': [{'Phone/Documents': 0}, {'Unique Base URLs': 0}, {'Archive/Document': 0}, {'URL/Documents': 0}, {'Document Count': 0}, {'Average Score': 0}, {'Updated 9 Days ago': 0}, {'Most Recent': '01 Dec'}, {'Email/Document': 0}, {'Oldest Update': '01 Dec'}, {'Updated 5 Days ago': 0}, {'Common Type': 'general'}], 'leak_model': [{'Most Recent': '01 Dec'}, {'Unique Base URLs': 0}, {'Dumps/Document': 0}, {'Updated 5 Days ago': 0}, {'Oldest Update': '01 Dec'}, {'URL/Documents': 0}, {'Document Count': 0}, {'Updated 9 Days ago': 0}]}"
  INSIGHT_STAT_DEFAULT = "{'generic_model': [{'Phone/Documents': {'value': 0, 'change': '+0.00%'}}, {'Unique Base URLs': {'value': 0, 'change': '+0.00%'}}, {'Archive/Document': {'value': 0, 'change': '+0.00%'}}, {'URL/Documents': {'value': 0, 'change': '+0.00%'}}, {'Document Count': {'value': 0, 'change': '+0.00%'}}, {'Average Score': {'value': 0, 'change': '+0.00%'}}, {'Updated 9 Days ago': {'value': 0, 'change': '+0.00%'}}, {'Most Recent': {'value': '0', 'change': '-'}}, {'Email/Document': {'value': 0, 'change': '+0.00%'}}, {'Oldest Update': {'value': '0', 'change': '-'}}, {'Updated 5 Days ago': {'value': 0, 'change': '+0.00%'}}, {'Common Type': {'value': 'general', 'change': '-'}}], 'leak_model': [{'Most Recent': {'value': '0', 'change': '-'}}, {'Unique Base URLs': {'value': 0, 'change': '+0.00%'}}, {'Dumps/Document': {'value': 0, 'change': '+0.00%'}}, {'Updated 5 Days ago': {'value': 0, 'change': '+0.00%'}}, {'Oldest Update': {'value': '0', 'change': '-'}}, {'URL/Documents': {'value': 0, 'change': '+0.00%'}}, {'Document Count': {'value': 0, 'change': '+0.00%'}}, {'Updated 9 Days ago': {'value': 0, 'change': '+0.00%'}}]}"

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
