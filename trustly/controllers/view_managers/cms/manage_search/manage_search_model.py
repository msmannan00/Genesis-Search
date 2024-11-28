import json

from bson import json_util
from django.shortcuts import render

from trustly.services.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS
from trustly.services.mongo_manager.mongo_controller import mongo_controller
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.enums import MONGO_COMMANDS
from trustly.controllers.view_managers.cms.manage_search.class_model.manage_search_model import manage_search_data_model
from trustly.controllers.view_managers.cms.manage_search.manage_search_enums import MANAGE_SEARCH_SESSION_COMMANDS, MANAGE_SEARCH_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.manage_search.manage_search_session_controller import manage_search_session_controller
from trustly.services.request_manager.request_handler import request_handler
from trustly.services.elastic_manager import elastic_controller
from trustly.services.mongo_manager.mongo_enums import MONGODB_CRUD


class manage_search_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = manage_search_session_controller()
        pass

    @staticmethod
    def get_requested_data(p_manage_search_model:manage_search_data_model):

        if p_manage_search_model.m_query_type == "mongo-DB":
            m_response, m_status = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_READ,[MONGO_COMMANDS.M_READ_RAW,[p_manage_search_model], [None,None]])
            if m_status is False:
                p_manage_search_model.m_query_error = m_response
            else:
                m_response = [doc for doc in m_response]
                p_manage_search_model.m_query_success = json.dumps(m_response, sort_keys=True, indent=4, default=json_util.default)

        if p_manage_search_model.m_query_type == "elastic-search":

            m_status, m_response = elastic_controller.elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.S_QUERY_RAW, [p_manage_search_model], [p_manage_search_model.m_min_range, p_manage_search_model.m_max_range]])
            if m_status is False:
                p_manage_search_model.m_query_error = m_response
            else:
                m_response = m_response['hits']['hits']
                p_manage_search_model.m_query_success = json.dumps(m_response, sort_keys=True, indent=4, default=json_util.default)

        return p_manage_search_model

    def __init_page(self, p_data):
        m_context,m_manage_search_model, m_status = self.__m_session.invoke_trigger(MANAGE_SEARCH_SESSION_COMMANDS.M_INIT, p_data)

        if m_status is True:
            m_manage_search_model = self.get_requested_data(m_manage_search_model)
            m_context = self.__m_session.invoke_trigger(MANAGE_SEARCH_SESSION_COMMANDS.M_VALIDATE,m_manage_search_model)
            return render(None, CONSTANTS.S_TEMPLATE_MANAGE_SEARCH_WEBSITE_PATH, m_context)
        else:
            return render(None, CONSTANTS.S_TEMPLATE_LOGIN_WEBSITE_PATH, m_context)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_SEARCH_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
