from django.middleware.csrf import get_token

from app_manager.mongo_manager.mongo_controller import mongo_controller
from app_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from trustly.controllers.constants.enums import MONGO_COMMANDS
from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.helper_manager.helper_controller import helper_controller
from trustly.controllers.view_managers.user.interactive.sitemap_manager.class_model.sitemap_data_model import sitemap_data_model
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_SESSION_COMMANDS, SITEMAP_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_session_controller import sitemap_session_controller
from app_manager.request_manager.request_handler import request_handler


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

        csrf_token = get_token(p_data)
        m_context_response["csrf_token"]=csrf_token
        return m_context_response, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
