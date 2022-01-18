import enum


class SEARCH_MODEL_COMMANDS(enum.Enum):
    M_INIT = 1

class USER_INDEX_MODEL_COMMANDS(enum.Enum):
    M_INIT = 1

class SEARCH_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    INIT_SEARCH_PARAMETER = 2
    M_VALIDATE = 3

class SEARCH_PARAM:
    M_QUERY = "q"
    M_TYPE = "pSearchParamType"
    M_PAGE = "mSearchParamPage"
    M_SAFE_SEARCH = "mSearchParamSafeSearch"
    M_SECURE_SERVICE = "pSite"

class SEARCH_CALLBACK:
    M_QUERY = "mSearchCallbackQuery"
    M_DOCUMENT = "mSearchCallbackRelevantDocument"
    M_TITLE = "mSearchCallbackRelevantDocumentTitle"
    M_URL = "mSearchCallbackRelevantDocumentURL"
    M_IMAGE_TYPE = "m_type"
    M_IMAGE_URL = "m_url"
    M_DESCRIPTION = "mSearchCallbackRelevantDocumentDescription"
    K_SEARCH_TYPE = "mSearchCallbackRelevantSearchType"
    M_MAX_PAGINATION = "mSearchCallbackMaxPagination"
    M_QUERY_ERROR = "mSearchCallbackQueryError"
    M_QUERY_ERROR_URL = "mSearchCallbackQueryErrorURL"
    M_PAGE_NUM = "mSearchCallbackPageNumber"
    M_SAFE_SEARCH = "mSearchCallbackSaveSearch"
    M_CURRENT_PAGE_NUM = "mSearchCallbackCurrentPageNumber"
    M_RESULT_COUNT = "mSearchCallbackResultCount"
    M_RELATED_BUSINESS_SITES = "mSearchCallbackRelevantBusiness"
    M_RELATED_NEWS_SITES = "mSearchCallbackRelevantDocumentNews"
    M_RELATED_FILES = "mSearchCallbackRelevantDocumentFiles"
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"

class SEARCH_DOCUMENT_CALLBACK:
    M_TITLE = "m_title"
    M_HOST = "m_host"
    M_SUB_HOST = "m_sub_host"
    M_IMPORTANT_DESCRIPTION = "m_important_content"
    M_CONTENT_TYPE = "m_content_type"
    M_IMAGE = "m_images"
    M_DOCUMENT = "m_doc_url"

class SEARCH_MODEL_SPELL_CHECKER(enum.Enum):
    M_CHECK_SPELLING = 1

class SEARCH_MODEL_TOKENIZATION_COMMANDS(enum.Enum):
    M_NORMALIZE = 1
    M_SPLIT_AND_NORMALIZE = 2
