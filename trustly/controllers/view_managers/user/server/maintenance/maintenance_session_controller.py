from trustly.controllers.view_managers.user.server.maintenance.maintenance_enums import MAINTENANCE_SESSION_COMMANDS, \
    MAINTENANCE_PARAM, MAINTENANCE_CALLBACK
from app_manager.request_manager.request_handler import request_handler


class maintenance_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_context = {
            MAINTENANCE_CALLBACK.M_SECURE_SERVICE_NOTICE:"http",
        }

        if MAINTENANCE_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_context[MAINTENANCE_CALLBACK.M_SECURE_SERVICE_NOTICE] = p_data.GET[MAINTENANCE_PARAM.M_SECURE_SERVICE]


        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == MAINTENANCE_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)

