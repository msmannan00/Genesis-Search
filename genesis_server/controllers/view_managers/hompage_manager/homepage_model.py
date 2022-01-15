from genesis_server.controllers.view_managers.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS, HOMEPAGE_SESSION_COMMANDS
from genesis_server.controllers.view_managers.hompage_manager.homepage_session_controller import homepage_session_controller
from genesis_shared_directory.request_manager.request_handler import request_handler


class homepage_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = homepage_session_controller()
        pass

    def __init_page(self):
        m_context, m_status = self.__m_session.invoke_trigger(HOMEPAGE_SESSION_COMMANDS.M_INIT, None)

        return m_context, m_status

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_MODEL_COMMANDS.M_INIT:
            return self.__init_page()
