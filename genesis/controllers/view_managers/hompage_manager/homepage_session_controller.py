from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.view_managers.hompage_manager.homepage_enums import HOMEPAGE_CALLBACK, HOMEPAGE_SESSION_COMMANDS
from genesis.controllers.request_manager.request_handler import request_handler


class homepage_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self):
        m_context = {
            HOMEPAGE_CALLBACK.M_REFERENCE: helper_controller.load_json(CONSTANTS.S_REFERENCE_WEBSITE_URL),
            HOMEPAGE_CALLBACK.M_IS_MOBILE: True
        }
        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters()

