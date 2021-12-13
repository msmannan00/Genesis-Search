import os


class constants:

    # General URL
    S_GENERAL_DEFAULT_LANGUAGE = "en"

    # Reference URL
    S_REFERENCE_WEBSITE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "\\raw\\ReferenceWebsites.json"

    # Template URL
    S_TEMPLATE_NOTICE_WEBSITE_REPORT = "../notice/?mNoticeParamType=report"
    S_TEMPLATE_NOTICE_WEBSITE_UPLOAD = "../notice/?mNoticeParamType=upload"
    S_TEMPLATE_INDEX_PATH = "GenesisCrawler/homepage/index.html"
    S_TEMPLATE_PARENT = "../"
    S_TEMPLATE_REPORT_WEBSITE_PATH = "GenesisCrawler/report/report.html"
    S_TEMPLATE_DIRECTORY_WEBSITE_PATH = "GenesisCrawler/directory/directory.html"
    S_TEMPLATE_NOTICE_WEBSITE_PATH = "GenesisCrawler/notice/notice.html"
    S_TEMPLATE_SITEMAP_WEBSITE_PATH = "GenesisCrawler/sitemap/sitemap.html"
    S_TEMPLATE_SEARCH_WEBSITE_PATH = "GenesisCrawler/search/search.html"

    # MongoDB Database
    S_MONGO_DATABASE_NAME = 'genesis'
    S_MONGO_DATABASE_URL = 27017
    S_MONGO_DATABASE_IP = 'localhost'
    S_MONGO_DATABASE_REPORT_DOCUMENT_NAME = 'reported_websites'
    S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME = 'submitted_websites'
    S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME = 'index_model'

    # Settings Constants
    S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH = 15
    S_SETTINGS_SEARCHED_DOCUMENT_SIZE = 15
    S_SETTINGS_SEARCHED_IMAGE_SIZE = 40
    S_SETTINGS_DIRECTORY_LIST_MAX_SIZE = 5000
