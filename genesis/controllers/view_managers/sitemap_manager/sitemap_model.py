
from genesis.controllers.constants.enums import MONGO_COMMANDS
from genesis.controllers.constants.strings import GENERAL_STRINGS
from genesis.controllers.service_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.shared_model.sitemap_data_model import sitemap_data_model
from genesis.controllers.view_managers.sitemap_manager.sitemap_session_controller import sitemap_session_controller
from genesis.controllers.view_managers.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS, SITEMAP_SESSION_COMMANDS


class sitemap_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = sitemap_session_controller()

    def __upload__website(self, p_sitemap_data_model:sitemap_data_model):
        mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_REPLACE, [MONGO_COMMANDS.M_UPLOAD_URL, [p_sitemap_data_model],[True]])

    def __init_page(self, p_data):
        m_sitemap_data_model = self.__m_session.invoke_trigger(SITEMAP_SESSION_COMMANDS.M_INIT, [p_data])
        m_sitemap_data_model, m_context_response, m_validity_status = self.__m_session.invoke_trigger(SITEMAP_SESSION_COMMANDS.M_VALIDATE, [m_sitemap_data_model])

        if m_validity_status is True and GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN in helper_controller.get_host(m_sitemap_data_model.m_url):
            self.__upload__website(m_sitemap_data_model)

        return m_context_response, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
