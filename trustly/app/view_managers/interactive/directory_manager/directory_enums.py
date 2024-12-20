import enum


class DIRECTORY_MODEL_COMMANDS(enum.Enum):
  M_INIT = 1
  M_FETCH_LIST = 2


class DIRECTORY_SESSION_COMMANDS(enum.Enum):
  M_PRE_INIT = 1
  M_INIT = 2


class DIRECTORY_PARAMS:
  M_PAGE_NUMBER = "page"
  M_CONTENT_TYPE = "content_type"
  M_SECURE_SERVICE = "pSite"


class DIRECTORY_CALLBACK:
  M_PAGE_NUMBER = "page"
  M_TOTAL_PAGES = "mTotalPage"
  M_ONION_LINKS = "mDirectoryCallbackLinks"
  M_MAX_PAGE_REACHED = "mDirectoryCallbackPageNumberMaxReached"
  M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
  M_START_PAGE = "mStartPage"
  M_ENDPAGE = "mEndPage"
  M_PAGINATION = "mPagination"


class DIRECTORY_MODEL_CALLBACK:
  M_ID = "mID"
  M_URL = "mURL"
  M_CONTENT_TYPE = "mContentType"
