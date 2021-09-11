import os


class constants:

    # General URL
    S_REFERENCE_WEBSITE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "\\raw\\ReferenceWebsites.json"
    S_NOTICE_WEBSITE_REPORT_SUCCESS = "../notice/?mNoticeType=report"
    S_NOTICE_WEBSITE_UPLOAD_SUCCESS = "../notice/?mNoticeType=upload"

    # General Paths
    S_INDEX_PATH = "GenesisCrawler/homepage/index.html"
    S_REPORT_WEBSITE_PATH = "GenesisCrawler/report/report.html"
    S_NOTICE_WEBSITE_PATH = "GenesisCrawler/notice/notice.html"
    S_SITEMAP_WEBSITE_PATH = "GenesisCrawler/sitemap/sitemap.html"
    S_SEARCH_WEBSITE_PATH = "GenesisCrawler/search/search.html"

    # MongoDB Database
    S_MONGO_DATABASE_NAME = 'genesis'
    S_MONGO_DATABASE_URL = 27017
    S_MONGO_DATABASE_IP = 'localhost'
    S_MONGO_DATABASE_REPORT_DOCUMENT_NAME = 'reported_websites'
    S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME = 'submitted_websites'
    S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME = 'index_model'

