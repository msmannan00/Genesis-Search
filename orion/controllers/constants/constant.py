import os
from pathlib import Path

class CONSTANTS:

    # General URL
    S_GENERAL_DEFAULT_LANGUAGE = "en"

    # Reference URL
    S_REFERENCE_WEBSITE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/reference_websites.json"
    S_DICTIONARY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/dictionary"
    S_STEMMED_DICTIONARY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/stemmed_dictionary"
    S_LOCAL_FILE_PATH = str(Path(__file__).parent.parent.parent.parent.parent) + "/user_crawler_directory"

    # Template URL
    S_TEMPLATE_INDEX_PATH = "orion/user/interactive/homepage/index.html"
    S_TEMPLATE_REPORT_WEBSITE_PATH = "orion/user/interactive/report/report.html"
    S_TEMPLATE_DIRECTORY_WEBSITE_PATH = "orion/user/interactive/directory/directory.html"
    S_TEMPLATE_NOTICE_WEBSITE_PATH = "orion/user/interactive/notice/notice.html"
    S_TEMPLATE_POLICY_WEBSITE_PATH = "orion/user/interactive/privacy/privacy.html"
    S_TEMPLATE_SECRET_KEY_WEBSITE_PATH = "orion/user/server/secretkey/secretkey.html"
    S_TEMPLATE_MAINTENANCE_WEBSITE_PATH = "orion/user/server/maintenance/maintenance.html"
    S_TEMPLATE_LOGIN_WEBSITE_PATH = "orion/cms/login/login.html"
    S_TEMPLATE_DASHBOARD_WEBSITE_PATH = "orion/cms/dashboard/dashboard.html"
    S_TEMPLATE_MANAGE_SEARCH_WEBSITE_PATH = "orion/cms/manage_search/manage_search.html"
    S_TEMPLATE_MANAGE_STATUS_WEBSITE_PATH = "orion/cms/manage_status/manage_status.html"
    S_TEMPLATE_ERROR_WEBSITE_PATH = "orion/user/server/error/error.html"
    S_TEMPLATE_SITEMAP_WEBSITE_PATH = "orion/user/interactive/sitemap/sitemap.html"
    S_TEMPLATE_SEARCH_WEBSITE_PATH = "orion/user/interactive/search/search.html"
    S_TEMPLATE_RESTRICTED_WEBSITE_PATH = "orion/user/server/block/restricted.html"
    S_TEMPLATE_INTELLIGENCE_WEBSITE_PATH = "orion/user/interactive/intelligence/intelligence.html"
    S_SSL_VERIFICATION_PATH = "orion/.well-known/pki-validation/D16CA9D0C6D8EB91CF2B6FA9CC2F3715.txt"
    S_DUPLICATE_CRAWL_URL_PATH = "orion/.well-known/pki-validation/D16CA9D0C6D8EB91CF2B6FA9CC2F3715.txt"
    S_BRIDGE_PATH = "orion/.well-known/bridges.txt"
    S_APP_ADS_PATH = "orion/.well-known/app-ads.txt"
    S_TEMPLATE_DOWNLOAD_WEBSITE_PATH = "orion/user/interactive/download/download.html"
    S_TEMPLATE_DOWNLOAD_IFRAME_WEBSITE_PATH = "orion/.well-known/url.txt"
    S_TEMPLATE_CRAWL_URL_COMPLETE_WEBSITE_PATH = "orion/.well-known/url_complete.txt"

    # Template URL 360
    S_360_TEMPLATE_INDEX_PATH = "orion/360user/interactive/homepage/index.html"
    S_360_TEMPLATE_REPORT_WEBSITE_PATH = "orion/360user/interactive/report/report.html"
    S_360_TEMPLATE_DIRECTORY_WEBSITE_PATH = "orion/360user/interactive/directory/directory.html"
    S_360_TEMPLATE_NOTICE_WEBSITE_PATH = "orion/360user/interactive/notice/notice.html"
    S_360_TEMPLATE_POLICY_WEBSITE_PATH = "orion/360user/interactive/privacy/privacy.html"
    S_360_TEMPLATE_SECRET_KEY_WEBSITE_PATH = "orion/360user/server/secretkey/secretkey.html"
    S_360_TEMPLATE_MAINTENANCE_WEBSITE_PATH = "orion/360user/server/maintenance/maintenance.html"
    S_360_TEMPLATE_ERROR_WEBSITE_PATH = "orion/360user/server/error/error.html"
    S_360_TEMPLATE_SITEMAP_WEBSITE_PATH = "orion/360user/interactive/sitemap/sitemap.html"
    S_360_TEMPLATE_SEARCH_WEBSITE_PATH = "orion/360user/interactive/search/search.html"
    S_360_TEMPLATE_BLOCK_WEBSITE_PATH = "orion/360user/server/block/block.html"
    S_360_TEMPLATE_INTELLIGENCE_WEBSITE_PATH = "orion/360user/interactive/intelligence/intelligence.html"
    S_360_TEMPLATE_DOWNLOAD_WEBSITE_PATH = "orion/360user/interactive/download/download.html"

    # Direct Links
    S_TEMPLATE_LOGIN_SHORT = "/cms/login"
    S_TEMPLATE_DASHBOARD_WEBSITE_SHORT = "/cms/dashboard"
    S_TEMPLATE_PARENT = "../"
    S_TEMPLATE_NOTICE_WEBSITE_REPORT = "../notice/?mNoticeParamType=report"
    S_TEMPLATE_NOTICE_WEBSITE_UPLOAD = "../notice/?mNoticeParamType=upload"

    # MongoDB Database
    S_MONGO_DATABASE_NAME = 'orion'
    S_MONGO_DATABASE_URL = 27017
    S_MONGO_DATABASE_IP = 'localhost'

    # Settings Constants
    S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH = 15
    S_SETTINGS_SEARCHED_DOCUMENT_SIZE = 15
    S_SETTINGS_MAX_PAGE_SIZE = 5
    S_SETTINGS_FETCHED_DOCUMENT_SIZE = 75
    S_SETTINGS_SEARCHED_IMAGE_SIZE = 40
    S_SETTINGS_DIRECTORY_LIST_MAX_SIZE = 5000
