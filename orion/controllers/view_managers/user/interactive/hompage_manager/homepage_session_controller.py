from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.constants.strings import GENERAL_STRINGS
from orion.controllers.helper_manager.helper_controller import helper_controller
from orion.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_CALLBACK, HOMEPAGE_PARAM, HOMEPAGE_SESSION_COMMANDS
from shared_directory.request_manager.request_handler import request_handler


class homepage_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_context = {
            HOMEPAGE_CALLBACK.M_REFERENCE: helper_controller.load_json(CONSTANTS.S_REFERENCE_WEBSITE_URL),
            HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE: GENERAL_STRINGS.S_GENERAL_HTTP
        }

        if HOMEPAGE_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_context[HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE] = p_data.GET[HOMEPAGE_PARAM.M_SECURE_SERVICE]

        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)

