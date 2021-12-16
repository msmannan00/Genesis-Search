
from genesis.constants.enums import MONGO_COMMANDS
from genesis.constants.strings import GENERAL_STRINGS
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_CRUD_COMMANDS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.shared_model.request_handler import request_handler
from genesis.controllers.sitemap_manager.sitemap_session_controller import sitemap_session_controller
from genesis.controllers.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, SITEMAP_CALLBACK, SITEMAP_PARAM, SITEMAP_SESSION_COMMANDS


class sitemap_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = sitemap_session_controller()

    def __upload__website(self, p_context):
        m_data = {
            SITEMAP_PARAM.M_URL: p_context[SITEMAP_CALLBACK.M_URL],
            SITEMAP_PARAM.M_EMAIL: p_context[SITEMAP_CALLBACK.M_EMAIL],
            SITEMAP_PARAM.M_NAME: p_context[SITEMAP_CALLBACK.M_NAME],
            SITEMAP_PARAM.M_KEYWORD: p_context[SITEMAP_CALLBACK.M_KEYWORD],
            SITEMAP_PARAM.M_SECRETKEY: p_context[SITEMAP_CALLBACK.M_SECRETKEY],
            SITEMAP_PARAM.M_URL.M_SUBMISSION_RULES: p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES],
        }

        mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_REPLACE, [MONGO_COMMANDS.M_UPLOAD_URL, m_data])

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(SITEMAP_SESSION_COMMANDS.M_INIT, [p_data])
        if m_status is False:
            return m_context, False

        m_context, m_status = self.__m_session.invoke_trigger(SITEMAP_SESSION_COMMANDS.M_VALIDATE, [m_context])
        if m_status is True and GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN in helper_controller.get_host(m_context[SITEMAP_CALLBACK.M_URL]):
            self.__upload__website(m_context)

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
