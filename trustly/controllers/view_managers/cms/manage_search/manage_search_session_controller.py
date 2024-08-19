from trustly.controllers.view_managers.cms.manage_search.class_model.manage_search_model import manage_search_data_model
from trustly.controllers.view_managers.cms.manage_search.manage_search_enums import MANAGE_SEARCH_SESSION_COMMANDS, MANAGE_SEARCH_PARAM, MANAGE_SEARCH_CALLBACK
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.session.session_enums import SESSION_KEYS


class manage_search_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_manage_search_model = manage_search_data_model()
        if SESSION_KEYS.S_USERNAME in p_data.session :
            if MANAGE_SEARCH_PARAM.M_MIN_RANGE in p_data.POST:
                m_manage_search_model.m_min_range = p_data.POST[MANAGE_SEARCH_PARAM.M_MIN_RANGE]
            if MANAGE_SEARCH_PARAM.M_MAX_RANGE in p_data.POST:
                m_manage_search_model.m_max_range = p_data.POST[MANAGE_SEARCH_PARAM.M_MAX_RANGE]
            if MANAGE_SEARCH_PARAM.M_SEARCH_TYPE in p_data.POST:
                m_manage_search_model.m_query_type = p_data.POST[MANAGE_SEARCH_PARAM.M_SEARCH_TYPE]
            if MANAGE_SEARCH_PARAM.M_QUERY in p_data.POST:
                m_manage_search_model.m_query = p_data.POST[MANAGE_SEARCH_PARAM.M_QUERY]
            if MANAGE_SEARCH_PARAM.M_QUERY_COLLECTION in p_data.POST:
                m_manage_search_model.m_query_collection = p_data.POST[MANAGE_SEARCH_PARAM.M_QUERY_COLLECTION]

            return {},m_manage_search_model, True
        else :
            return {},None, False

    def init_callbacks(self, p_manage_search_model:manage_search_data_model):
        m_context_response = {
            MANAGE_SEARCH_CALLBACK.M_MIN_RANGE: p_manage_search_model.m_min_range,
            MANAGE_SEARCH_CALLBACK.M_MAX_RANGE: p_manage_search_model.m_max_range,
            MANAGE_SEARCH_CALLBACK.M_SEARCH_TYPE: p_manage_search_model.m_query_type,
            MANAGE_SEARCH_CALLBACK.M_QUERY_COLLECTION: p_manage_search_model.m_query_collection,
            MANAGE_SEARCH_CALLBACK.M_QUERY: p_manage_search_model.m_query,
            MANAGE_SEARCH_CALLBACK.M_QUERY_ERROR: p_manage_search_model.m_query_error,
            MANAGE_SEARCH_CALLBACK.M_QUERY_SUCCESS: p_manage_search_model.m_query_success
        }

        return m_context_response
    def __validate_parameters(self, p_manage_search_model:manage_search_data_model):
        m_context_response = self.init_callbacks(p_manage_search_model)
        return m_context_response

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_SEARCH_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)
        if p_command == MANAGE_SEARCH_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data)

