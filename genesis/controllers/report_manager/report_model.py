
from genesis.constants.enums import MONGO_COMMANDS
from genesis.constants.strings import GENERAL_STRINGS
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_CRUD_COMMANDS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.report_manager.report_enums import REPORT_MODEL_COMMANDS, REPORT_CALLBACK, REPORT_PARAM, REPORT_SESSION_COMMANDS
from genesis.controllers.report_manager.report_session_controller import report_session_controller
from genesis.controllers.shared_model.request_handler import request_handler

class report_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = report_session_controller()
        pass

    def __upload_website(self, p_context):
        m_data = {
            REPORT_PARAM.M_URL: p_context[REPORT_CALLBACK.M_URL],
            REPORT_PARAM.M_EMAIL: p_context[REPORT_CALLBACK.M_EMAIL],
            REPORT_PARAM.M_MESSAGE: p_context[REPORT_CALLBACK.M_MESSAGE],
        }

        mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_CREATE, [MONGO_COMMANDS.M_REPORT_URL, m_data])

    def __init_page(self, p_data):

        m_context, m_status = self.__m_session.invoke_trigger(REPORT_SESSION_COMMANDS.M_INIT, [p_data])
        if m_status is False:
            return m_context, False

        m_context, m_status = self.__m_session.invoke_trigger(REPORT_SESSION_COMMANDS.M_VALIDATE, [m_context])
        if m_status is True and GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN in helper_controller.get_host(m_context[REPORT_CALLBACK.M_URL]):
            self.__upload_website(m_context)
            m_context = {}

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == REPORT_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
