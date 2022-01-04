from genesis.controllers.constants.enums import MONGO_COMMANDS
from genesis.controllers.service_manager.mongo_manager.mongo_enums import MONGODB_COLLECTIONS, MONGODB_KEYS
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.shared_model.report_data_model import report_data_model
from genesis.controllers.shared_model.sitemap_data_model import sitemap_data_model


class mongo_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_report_url(self, p_report_data_model:report_data_model):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_REPORT, MONGODB_KEYS.S_VALUE:{"m_url": p_report_data_model.m_url,"m_email": p_report_data_model.m_email,"m_message": p_report_data_model.m_message}}

    def __on_upload_url(self, p_sitemap_data_model:sitemap_data_model):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{"m_url": { "$eq": p_sitemap_data_model.m_url }},MONGODB_KEYS.S_VALUE:{"m_email":p_sitemap_data_model.m_email, "m_name": p_sitemap_data_model.m_name, "m_keyword":p_sitemap_data_model.m_keyword, "m_secret_key":p_sitemap_data_model.m_secret_key, "m_submission_rule":p_sitemap_data_model.m_submission_rule}}

    def __on_fetch_service_by_url(self, p_url):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{"m_url": p_url}}

    def __on_fetch_secret_key(self, p_secret_key):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{'m_secret_key':p_secret_key}}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGO_COMMANDS.M_REPORT_URL:
            return self.__on_report_url(p_data[0])
        if p_commands == MONGO_COMMANDS.M_UPLOAD_URL:
            return self.__on_upload_url(p_data[0])
        if p_commands == MONGO_COMMANDS.M_FIND_URL:
            return self.__on_fetch_service_by_url(p_data)
        if p_commands == MONGO_COMMANDS.M_FIND_SECRET_KEY:
            return self.__on_fetch_secret_key(p_data[0])

