import math
import time

from Genesis.controllers.constants.enums import MONGO_COMMANDS
from Genesis.controllers.view_managers.user.interactive.report_manager.class_model.report_data_model import report_data_model
from Genesis.controllers.view_managers.user.interactive.sitemap_manager.class_model.sitemap_data_model import sitemap_data_model
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_KEYS, MONGODB_COLLECTIONS


class mongo_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_verify_credentials(self, p_username, p_password):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{"m_username": {'$eq': p_username}, "m_password": {'$eq': p_password}}}

    def __on_report_url(self, p_report_data_model:report_data_model):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_REPORT, MONGODB_KEYS.S_VALUE:{"m_url": p_report_data_model.m_url,"m_email": p_report_data_model.m_email,"m_message": p_report_data_model.m_message}}

    def __on_upload_url(self, p_sitemap_data_model:sitemap_data_model):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{"m_url": { "$eq": p_sitemap_data_model.m_url }},MONGODB_KEYS.S_VALUE:{"m_email":p_sitemap_data_model.m_email, "m_name": p_sitemap_data_model.m_name, "m_keyword":p_sitemap_data_model.m_keyword, "m_secret_key":p_sitemap_data_model.m_secret_key, "m_submission_rule":p_sitemap_data_model.m_submission_rule}}

    def __on_fetch_service_by_url(self, p_url):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{"m_url": p_url}}

    def __on_fetch_secret_key(self, p_secret_key):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{'m_secret_key':p_secret_key}}

    def __on_update_status(self, m_name):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_STATUS, MONGODB_KEYS.S_FILTER:{},MONGODB_KEYS.S_VALUE:{"$set": {m_name:(math.ceil(time.time()/60))}}}


    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGO_COMMANDS.M_VERIFY_CREDENTIAL:
            return self.__on_verify_credentials(p_data[0], p_data[1])
        if p_commands == MONGO_COMMANDS.M_REPORT_URL:
            return self.__on_report_url(p_data[0])
        if p_commands == MONGO_COMMANDS.M_UPLOAD_URL:
            return self.__on_upload_url(p_data[0])
        if p_commands == MONGO_COMMANDS.M_FIND_URL:
            return self.__on_fetch_service_by_url(p_data)
        if p_commands == MONGO_COMMANDS.M_FIND_SECRET_KEY:
            return self.__on_fetch_secret_key(p_data[0])
        if p_commands == MONGO_COMMANDS.M_UPDATE_STATUS:
            return self.__on_update_status(p_data[0])

