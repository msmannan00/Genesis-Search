from genesis.constants.enums import MONGO_COMMANDS
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_COLLECTIONS, MONGODB_KEYS
from genesis.controllers.shared_model.request_handler import request_handler
from genesis.controllers.sitemap_manager.sitemap_enums import SITEMAP_PARAM


class mongo_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_report_url(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_REPORT, MONGODB_KEYS.S_FILTER:{}}

    def __on_upload_url(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER:{'pSecretKey': p_data[SITEMAP_PARAM.M_URL.M_SECRET_KEY]}, MONGODB_KEYS.S_VALUE:p_data[1]}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGO_COMMANDS.M_REPORT_URL:
            self.__on_report_url()
        if p_commands == MONGO_COMMANDS.M_UPLOAD_URL:
            self.__on_upload_url(p_data)
