import json

from trustly.controllers.server_manager.crawl_index_manager.class_model.crawl_model import crawl_model
from trustly.controllers.server_manager.crawl_index_manager.crawl_enums import CRAWL_PARAM, CRAWL_COMMANDS
from app_manager.request_manager.request_handler import request_handler


class crawl_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_crawl_model = crawl_model()

        if CRAWL_PARAM.M_CRAWL_REQUEST_COMMAND in p_data.POST:
            m_crawl_model.m_command = int(p_data.POST[CRAWL_PARAM.M_CRAWL_REQUEST_COMMAND])
        if CRAWL_PARAM.M_CRAWL_REQUEST_DATA in p_data.POST:
            m_crawl_model.m_data = json.loads(p_data.POST[CRAWL_PARAM.M_CRAWL_REQUEST_DATA])

        if m_crawl_model.m_command is None or m_crawl_model.m_data is None:
            return False, m_crawl_model
        else:
            return True, m_crawl_model

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == CRAWL_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)