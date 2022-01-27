from Genesis.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK, ERROR_SESSION_COMMANDS
from Genesis.controllers.view_managers.user.server.error.error_session_controller import error_session_controller
from shared_directory.request_manager.request_handler import request_handler


class error_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = error_session_controller()
        pass

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(ERROR_SESSION_COMMANDS.M_INIT, p_data)

        return m_context, m_status

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == ERROR_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
