from app_manager.session_manager.session_controller import session_controller
from trustly.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_SESSION_COMMANDS
from app_manager.request_manager.request_handler import request_handler
from app_manager.session_manager.session_enums import SESSION_KEYS, SESSION_COMMANDS


class dashboard_session_controller(request_handler):

    # Helper Methods

    def __init_parameters(self, p_data):
        m_status = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS, p_data)
        if SESSION_KEYS.S_USERNAME in p_data.session :
            return {}, m_status
        else :
            return {}, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DASHBOARD_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)

