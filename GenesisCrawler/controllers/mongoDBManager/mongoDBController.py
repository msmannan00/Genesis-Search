# Local Imports
import pymongo

from GenesisCrawler.constants import strings
from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.keys import K_MONGO_SITEMAP_SUBMISSION_RULE, K_MONGO_SITEMAP_SECRET_KEY, \
    K_MONGO_SITEMAP_URL, K_MONGO_REPORT_URL


class mongoDBController:

    # Local Variables
    __instance = None
    m_connection = None

    # Initializations
    @staticmethod
    def getInstance():
        if mongoDBController.__instance is None:
            mongoDBController()
        return mongoDBController.__instance

    def __init__(self):
        mongoDBController.__instance = self
        self.linkConnection()

    def linkConnection(self):
        self.m_connection = pymongo.MongoClient(constants.S_MONGO_DATABASE_IP, constants.S_MONGO_DATABASE_URL)[constants.S_MONGO_DATABASE_NAME]

    def onReportURL(self, pData):
        try:
            m_collection = self.m_connection[constants.S_MONGO_DATABASE_REPORT_DOCUMENT_NAME]
            m_collection.insert_one(pData)
        except Exception:
            pass

    def getWebsiteFromURL(self, pData):
        try:
            m_collection = self.m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {K_MONGO_SITEMAP_URL: pData[K_MONGO_SITEMAP_URL]}
            mResult = m_collection.find_one(mFilter)
            return mResult
        except Exception as e:
            return None

    def getWebsiteFromKey(self, pData):
        try:
            m_collection = self.m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {K_MONGO_SITEMAP_SECRET_KEY: pData[K_MONGO_SITEMAP_SECRET_KEY]}
            mResult = m_collection.find_one(mFilter)
            return mResult
        except Exception as e:
            return None

    def onUploadURL(self, pData):
        try:
            m_collection = self.m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {'pSecretKey': pData[K_MONGO_SITEMAP_SECRET_KEY]}
            m_collection.replace_one(mFilter, pData, True)
        except Exception as e:
            pass

    def onSearchResult(self, pData):
        try:
            m_collection = self.m_connection[constants.S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME]
            mResult = m_collection.find({"$text": {"$search": "accept"}})

            for document in mResult:
                print(document)

            print(mResult.collection)

        except Exception as e:
            print(e)
            pass

    # External Request Callbacks
    def invokeTrigger(self, pCommands, pData):
        if pCommands == MongoDBCommands.M_REPORT_URL:
            self.onReportURL(pData)
        if pCommands == MongoDBCommands.M_UPLOAD_URL:
            self.onUploadURL(pData)
        if pCommands == MongoDBCommands.M_FIND_URL:
            return self.getWebsiteFromURL(pData)
        if pCommands == MongoDBCommands.M_FIND_SECRET_KEY:
            return self.getWebsiteFromKey(pData)
        if pCommands == MongoDBCommands.M_SEARCH:
            return self.onSearchResult(pData)

