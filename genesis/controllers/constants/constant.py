import os


class CONSTANTS:

    # General URL
    S_GENERAL_DEFAULT_LANGUAGE = "en"

    # Reference URL
    S_REFERENCE_WEBSITE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                           "../..")) + "\\raw\\reference_websites.json"
    S_DICTIONARY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "\\raw\\dictionary"

    # Template URL
    S_TEMPLATE_NOTICE_WEBSITE_REPORT = "../notice/?mNoticeParamType=report"
    S_TEMPLATE_NOTICE_WEBSITE_UPLOAD = "../notice/?mNoticeParamType=upload"
    S_TEMPLATE_INDEX_PATH = "genesis/homepage/index.html"
    S_TEMPLATE_PARENT = "../"
    S_TEMPLATE_REPORT_WEBSITE_PATH = "genesis/report/report.html"
    S_TEMPLATE_DIRECTORY_WEBSITE_PATH = "genesis/directory/directory.html"
    S_TEMPLATE_NOTICE_WEBSITE_PATH = "genesis/notice/notice.html"
    S_TEMPLATE_SITEMAP_WEBSITE_PATH = "genesis/sitemap/sitemap.html"
    S_TEMPLATE_SEARCH_WEBSITE_PATH = "genesis/search/search.html"

    # MongoDB Database
    S_MONGO_DATABASE_NAME = 'genesis'
    S_MONGO_DATABASE_URL = 27017
    S_MONGO_DATABASE_IP = 'localhost'

    # Settings Constants
    S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH = 15
    S_SETTINGS_SEARCHED_DOCUMENT_SIZE = 15
    S_SETTINGS_MAX_PAGE_SIZE = 5
    S_SETTINGS_FETCHED_DOCUMENT_SIZE = 75
    S_SETTINGS_SEARCHED_IMAGE_SIZE = 40
    S_SETTINGS_DIRECTORY_LIST_MAX_SIZE = 5000
