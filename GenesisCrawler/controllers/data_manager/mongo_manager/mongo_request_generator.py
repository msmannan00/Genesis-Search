from bson import ObjectId

from GenesisCrawler.constants.enums import MONGO_COMMANDS
from GenesisCrawler.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_COLLECTIONS, MONGODB_KEYS
from GenesisCrawler.controllers.shared_model.request_handler import request_handler
from GenesisCrawler.controllers.sitemap_manager.sitemap_enums import SITEMAP_PARAM


class mongo_request_generator(request_handler):

    def __init__(self):
        pass


    def __fetch_total_documents(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __on_report_url(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_REPORT, MONGODB_KEYS.S_FILTER:{}}

    def __on_upload_url(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{'pSecretKey': p_data[SITEMAP_PARAM.M_URL.M_SECRET_KEY]}, MONGODB_KEYS.S_VALUE:p_data[1]}

    def __on_fetch_service_by_url(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{SITEMAP_PARAM.M_URL: p_data[SITEMAP_PARAM.M_URL]}}

    def __on_fetch_secret_key(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{SITEMAP_PARAM.M_SECRET_KEY: p_data[SITEMAP_PARAM.M_URL.M_SECRET_KEY]}}

    def __on_fetch_service_by_token(self, p_tokens_list, p_query_model):
        m_word_filter = []

        for m_tokens in p_tokens_list:
            m_word_filter.append({"m_uniary_tfidf_score." + m_tokens: {"$exists": True}})

        m_filter = []
        m_safe_search_status = p_query_model.m_safe_search


        if p_query_model.m_search_type != "all":
            m_filter.append({"$match": {'m_content_type': {"$eq": p_query_model.m_search_type[0], }}})
        elif m_safe_search_status == 'True':
            m_filter.append({"$match": {'m_content_type': {"$ne": 'a', }}})


        m_filter.append({"$match": {"$or":m_word_filter}})
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:m_filter}

    def __on_fetch_known_services(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{"$and": [{"$or": [{"m_url": {"$regex": "onion$"}}, {"m_url": {"$regex": "onion/$"}}]},{"m_url": {"$not": {"$regex": "\?"}}}]}}

    def __fetch_service_by_id(self, p_id):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{"_id": ObjectId(p_id)}}


    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGO_COMMANDS.M_TOTAL_DOCUMENTS:
            return self.__fetch_total_documents()
        if p_commands == MONGO_COMMANDS.M_REPORT_URL:
            self.__on_report_url(p_data)
        if p_commands == MONGO_COMMANDS.M_UPLOAD_URL:
            self.__on_upload_url(p_data)
        if p_commands == MONGO_COMMANDS.M_FIND_URL:
            return self.__on_fetch_service_by_url(p_data)
        if p_commands == MONGO_COMMANDS.M_FIND_SECRET_KEY:
            return self.__on_fetch_secret_key(p_data)
        if p_commands == MONGO_COMMANDS.M_SEARCH_BY_TOKEN:
            return self.__on_fetch_service_by_token(p_data[0], p_data[1])
        if p_commands == MONGO_COMMANDS.M_ONION_LIST:
            return self.__on_fetch_known_services()
        if p_commands == MONGO_COMMANDS.M_FETCH_DOCUMENT_BY_ID:
            return self.__fetch_service_by_id(p_data[1])
