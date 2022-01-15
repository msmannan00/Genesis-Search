
from genesis_server.controllers.constants.enums import MONGO_COMMANDS
from genesis_server.controllers.constants.strings import GENERAL_STRINGS
from genesis_shared_directory.service_manager.mongo_manager.mongo_controller import mongo_controller
from genesis_shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from genesis_server.controllers.helper_manager.helper_controller import helper_controller
from genesis_server.controllers.view_managers.report_manager.report_enums import REPORT_MODEL_COMMANDS, REPORT_CALLBACK, \
    REPORT_SESSION_COMMANDS
from genesis_server.controllers.view_managers.report_manager.report_session_controller import report_session_controller
from genesis_shared_directory.request_manager.request_handler import request_handler

class report_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = report_session_controller()
        pass

    def __report_website(self, m_report_data_model):
        mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_CREATE, [MONGO_COMMANDS.M_REPORT_URL, [m_report_data_model],[True]])

    def __init_page(self, p_data):

        m_report_data_model = self.__m_session.invoke_trigger(REPORT_SESSION_COMMANDS.M_INIT, [p_data])
        m_report_data_model, m_context, m_status = self.__m_session.invoke_trigger(REPORT_SESSION_COMMANDS.M_VALIDATE, [m_report_data_model])
        if m_status is True and GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN in helper_controller.get_host(m_context[REPORT_CALLBACK.M_URL]):
            self.__report_website(m_report_data_model)
            m_context = {}

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
