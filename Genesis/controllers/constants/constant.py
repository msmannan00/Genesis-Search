import os
from pathlib import Path


class APP_STATUS:
    S_DEVELOPER = True
    S_FERNET_KEY = "W#ZYBHQa9G_DB_iU@yjA3Es@COu4-UzU"
    S_APP_BLOCK_KEY = "D~S=05y68#M25oj]vprm}9HE))Tr'VX?[p|m-Wg`mrg^"
    S_MAINTAINANCE = False

class CONSTANTS:

    # General URL
    S_GENERAL_DEFAULT_LANGUAGE = "en"

    # Reference URL
    S_REFERENCE_WEBSITE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/reference_websites.json"
    S_DICTIONARY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/dictionary"
    S_STEMMED_DICTIONARY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/raw/stemmed_dictionary"
    S_LOCAL_FILE_PATH = str(Path(__file__).parent.parent.parent.parent) + "/genesis_shared_directory/" + "ftp-directory"

    # Template URL
    S_TEMPLATE_NOTICE_WEBSITE_REPORT = "../notice/?mNoticeParamType=report"
    S_TEMPLATE_NOTICE_WEBSITE_UPLOAD = "../notice/?mNoticeParamType=upload"
    S_TEMPLATE_INDEX_PATH = "Genesis/homepage/index.html"
    S_TEMPLATE_PARENT = "../"
    S_TEMPLATE_REPORT_WEBSITE_PATH = "Genesis/report/report.html"
    S_TEMPLATE_DIRECTORY_WEBSITE_PATH = "Genesis/directory/directory.html"
    S_TEMPLATE_NOTICE_WEBSITE_PATH = "Genesis/notice/notice.html"
    S_TEMPLATE_POLICY_WEBSITE_PATH = "Genesis/privacy/privacy.html"
    S_TEMPLATE_SECRET_KEY_WEBSITE_PATH = "Genesis/secretkey/secretkey.html"
    S_TEMPLATE_MAINTENANCE_WEBSITE_PATH = "Genesis/maintenance/maintenance.html"
    S_TEMPLATE_SITEMAP_WEBSITE_PATH = "Genesis/sitemap/sitemap.html"
    S_TEMPLATE_SEARCH_WEBSITE_PATH = "Genesis/search/search.html"
    S_TEMPLATE_BLOCK_WEBSITE_PATH = "Genesis/block/block.html"

    # MongoDB Database
    S_MONGO_DATABASE_NAME = 'Genesis'
    S_MONGO_DATABASE_URL = 27017
    S_MONGO_DATABASE_IP = 'localhost'

    # Settings Constants
    S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH = 15
    S_SETTINGS_SEARCHED_DOCUMENT_SIZE = 15
    S_SETTINGS_MAX_PAGE_SIZE = 5
    S_SETTINGS_FETCHED_DOCUMENT_SIZE = 75
    S_SETTINGS_SEARCHED_IMAGE_SIZE = 40
    S_SETTINGS_DIRECTORY_LIST_MAX_SIZE = 5000
