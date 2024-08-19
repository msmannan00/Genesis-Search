from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_enums import NOTICE_CALLBACK, NOTICE_PARAM, NOTICE_SESSION_CALLBACK
from shared_directory.request_manager.request_handler import request_handler


class notice_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        # Local Variables
        m_status = False
        m_browser = False

        # Default Initialization
        m_context = {
            NOTICE_CALLBACK.M_TYPE: GENERAL_STRINGS.S_GENERAL_EMPTY,
            NOTICE_CALLBACK.M_DATA: GENERAL_STRINGS.S_GENERAL_EMPTY,
        }

        # Notice Header Param
        if NOTICE_PARAM.M_HEADER in p_data.GET:
            m_context[NOTICE_CALLBACK.M_TYPE] = p_data.GET[NOTICE_PARAM.M_HEADER]
            m_status = True

        # Notice Data Param
        if NOTICE_PARAM.M_BROWSER in p_data.GET and p_data.GET[NOTICE_PARAM.M_BROWSER] == "360wise":
            m_browser = True

        if NOTICE_PARAM.M_DATA in p_data.GET:
            m_context[NOTICE_CALLBACK.M_DATA] = p_data.GET[NOTICE_PARAM.M_DATA]

        return m_context, m_status, m_browser

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NOTICE_SESSION_CALLBACK.M_INIT:
            return self.__init_parameters(p_data[0])

