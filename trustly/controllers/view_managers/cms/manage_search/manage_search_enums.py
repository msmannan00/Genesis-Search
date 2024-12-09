import enum


class MANAGE_SEARCH_MODEL_CALLBACK(enum.Enum):
  M_INIT = 1


class MANAGE_SEARCH_SESSION_COMMANDS(enum.Enum):
  M_INIT = 1
  M_VALIDATE = 2


class MANAGE_SEARCH_PARAM:
  M_MIN_RANGE = "pMinRange"
  M_MAX_RANGE = "pMaxRange"
  M_SEARCH_TYPE = "pSearchType"
  M_QUERY = "pQuery"
  M_QUERY_COLLECTION = "pQueryCollection"


class MANAGE_SEARCH_CALLBACK:
  M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
  M_MIN_RANGE = "mMinRange"
  M_MAX_RANGE = "mMaxRange"
  M_SEARCH_TYPE = "mSearchType"
  M_QUERY_COLLECTION = "mQueryCollection"
  M_QUERY_ERROR = "mQueryError"
  M_QUERY_SUCCESS = "mQuerySuccess"
  M_QUERY = "mQuery"
