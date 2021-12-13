import enum


class SearchModelCommands(enum.Enum):
    M_INIT = 1

class SearchSessionCommands(enum.Enum):
    M_INIT = 1
    INIT_SEARCH_PARAMETER = 2
    M_VALIDATE = 3

class SearchParam(str, enum.Enum):
    M_QUERY = "q"
    M_TYPE = "pSearchParamType"
    M_PAGE = "mSearchParamPage"
    M_SAFE_SEARCH = "mSearchParamSafeSearch"

class SearchCallback(str, enum.Enum):
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
    M_PAGE_NUM = "mSearchCallbackPageNumber"
    M_SAFE_SEARCH = "mSearchCallbackSaveSearch"
    M_CURRENT_PAGE_NUM = "mSearchCallbackCurrentPageNumber"
    M_RESULT_COUNT = "mSearchCallbackResultCount"
    M_RELATED_BUSINESS_SITES = "mSearchCallbackRelevantBusiness"
    M_RELATED_NEWS_SITES = "mSearchCallbackRelevantDocumentNews"
    M_RELATED_FILES = "mSearchCallbackRelevantDocumentFiles"

class SearchDocumentCallback(str, enum.Enum):
    M_TITLE = "m_title"
    M_URL = "m_url"
    M_DESCRIPTION = "m_description"
    M_CONTENT_TYPE = "m_content_type"
    M_IMAGE = "m_images"

class SearchModelSpellCheckerCommands(enum.Enum):
    M_CHECK_SPELLING = 1

class SearchModelTokenizerCommands(enum.Enum):
    M_TOKENIZE = 1
