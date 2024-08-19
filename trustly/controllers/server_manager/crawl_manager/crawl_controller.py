import json

from django.http import HttpResponse

from trustly.controllers.server_manager.crawl_manager.crawl_enums import CRAWL_COMMANDS, CRAWL_ERROR_CALLBACK
from trustly.controllers.server_manager.crawl_manager.crawl_session_controller import crawl_session_controller
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.elastic_manager.elastic_controller import elastic_controller


class crawl_controller(request_handler):

    # Private Variables
    __instance = None
    __m_session = None


    # Initializations
    @staticmethod
    def getInstance():
        if crawl_controller.__instance is None:
            crawl_controller()
        return crawl_controller.__instance

    def __init__(self):
        if crawl_controller.__instance is not None:
            pass
        else:
            crawl_controller.__instance = self
            self.__m_session = crawl_session_controller()

    def __handle_request(self, p_data):

        m_status, m_crawl_model = self.__m_session.invoke_trigger(CRAWL_COMMANDS.M_INIT, p_data)
        if m_status is False:
            m_context = [False,CRAWL_ERROR_CALLBACK.M_INVALID_PARAM]
            return HttpResponse(m_context)
        else:
            m_response, m_data = elastic_controller.get_instance().invoke_trigger(m_crawl_model.m_command, m_crawl_model.m_data)
            m_context = [m_response,m_data]

            return HttpResponse(json.dumps(m_context))

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == CRAWL_COMMANDS.M_INIT:
            return self.__handle_request(p_data)

