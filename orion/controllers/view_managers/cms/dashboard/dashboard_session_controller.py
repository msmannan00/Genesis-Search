from orion.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_SESSION_COMMANDS
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.session.session_enums import SESSION_KEYS


class dashboard_session_controller(request_handler):

    # Helper Methods

    def __init_parameters(self, p_data):
        if SESSION_KEYS.S_USERNAME in p_data.session :
            return {}, True
        else :
            return {}, False

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DASHBOARD_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)

