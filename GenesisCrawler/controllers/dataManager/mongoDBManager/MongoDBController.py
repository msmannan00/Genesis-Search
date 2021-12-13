# Local Imports
import pymongo
from bson import ObjectId

from GenesisCrawler.constants import strings
from GenesisCrawler.constants.constant import constants
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapParam


class MongoDBController:

    # Local Variables
    __instance = None
    __m_connection = None

    # Initializations
    @staticmethod
    def getInstance():
        if MongoDBController.__instance is None:
            MongoDBController()
        return MongoDBController.__instance

    def __init__(self):
        MongoDBController.__instance = self
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = pymongo.MongoClient(constants.S_MONGO_DATABASE_IP, constants.S_MONGO_DATABASE_URL)[constants.S_MONGO_DATABASE_NAME]

    def __get_service_by_url(self, p_data):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {SitemapParam.M_URL: p_data[SitemapParam.M_URL]}
            mResult = m_collection.find_one(mFilter)
            return mResult
        except Exception:
            return None

    def __get_service_by_key(self, p_data):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {SitemapParam.M_SECRET_KEY: p_data[SitemapParam.M_URL.M_SECRET_KEY]}
            mResult = m_collection.find_one(mFilter)
            return mResult
        except Exception:
            return None

    def __get_service_by_token(self, p_tokens_list, p_query_model):

        m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME]

        m_word_filter = []

        for m_tokens in p_tokens_list:
            m_word_filter.append({"m_uniary_tfidf_score." + m_tokens: {"$exists": True}})

        m_filter = []
        m_safe_search_status = p_query_model.get_safe_search_status()


        if p_query_model.get_search_type() != "all":
            m_filter.append({"$match": {'m_content_type': {"$eq": p_query_model.get_search_type_mapped()[0], }}})
        elif m_safe_search_status is 'True':
            m_filter.append({"$match": {'m_content_type': {"$ne": 'a', }}})


        m_filter.append({"$match": {"$or":m_word_filter}})

        mResult = m_collection.aggregate(m_filter)

        return mResult

    def __get_service_by_id(self, p_relevance_list, p_type):
        try:
            mRelevanceListData = []
            mCount = 0
            for m_website in p_relevance_list:
                m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME]
                mFilter = {"_id": ObjectId(m_website.get_document_id())}
                mResult = m_collection.find_one(mFilter)
                mRelevanceListData.append(mResult)
                mCount+=1
            return mRelevanceListData
        except Exception:
            pass

    def __get_all_services(self, p_page):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME]
            m_filter = {"$and": [{"$or": [{"m_url": {"$regex": "onion$"}}, {"m_url": {"$regex": "onion/$"}}]},{"m_url": {"$not": {"$regex": "\?"}}}]}

            mResult = m_collection.find(m_filter)#.skip((p_page-1)*constants.S_SETTINGS_ONION_LIST_MAX_SIZE).limit(constants.S_SETTINGS_ONION_LIST_MAX_SIZE + 1)

            return mResult
        except Exception as e:
            return None

    def __upload_url(self, p_data):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SUBMIT_DOCUMENT_NAME]
            mFilter = {'pSecretKey': p_data[SitemapParam.M_URL.M_SECRET_KEY]}
            m_collection.replace_one(mFilter, p_data, True)
        except Exception:
            pass

    def __report_url(self, p_data):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_REPORT_DOCUMENT_NAME]
            m_collection.insert_one(p_data)
        except Exception:
            pass

    def __get_total_count(self):
        try:
            m_collection = self.__m_connection[constants.S_MONGO_DATABASE_SEARCH_DOCUMENT_NAME]
            return m_collection.find().count()
        except Exception:
            pass

    # External Request Callbacks
    def invoke_trigger(self, p_commands, p_data):
        if p_commands == MongoDBCommands.M_REPORT_URL:
            self.__report_url(p_data)
        if p_commands == MongoDBCommands.M_UPLOAD_URL:
            self.__upload_url(p_data)
        if p_commands == MongoDBCommands.M_FIND_URL:
            return self.__get_service_by_url(p_data)
        if p_commands == MongoDBCommands.M_FIND_SECRET_KEY:
            return self.__get_service_by_key(p_data)
        if p_commands == MongoDBCommands.M_SEARCH:
            return self.__get_service_by_token(p_data[0], p_data[1])
        if p_commands == MongoDBCommands.M_TOTAL_DOCUMENTS:
            return self.__get_total_count()
        if p_commands == MongoDBCommands.M_FETCH_DOCUMENTS:
            return self.__get_service_by_id(p_data[0], p_data[1])
        if p_commands == MongoDBCommands.M_ONION_LIST:
            return self.__get_all_services(p_data[0])
