from django.shortcuts import render
from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.constants.enums import MONGO_COMMANDS
from orion.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_MODEL_CALLBACK, MANAGE_STATUS_SESSION_COMMANDS
from orion.controllers.view_managers.cms.manage_status.manage_status_session_controller import manage_status_session_controller
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.mongo_manager.mongo_controller import mongo_controller
from shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD


class manage_status_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = manage_status_session_controller()
        pass

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(MANAGE_STATUS_SESSION_COMMANDS.M_INIT, p_data)
        if m_status is True:
            m_response, m_status = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_READ,[MONGO_COMMANDS.M_FETCH_STATUS, [], [None,None]])
            m_result = next(m_response, None)
            m_context = self.__m_session.invoke_trigger(MANAGE_STATUS_SESSION_COMMANDS.M_VALIDATE, m_result)

            return render(None, CONSTANTS.S_TEMPLATE_MANAGE_STATUS_WEBSITE_PATH, m_context)
        else:
            return render(None, CONSTANTS.S_TEMPLATE_LOGIN_WEBSITE_PATH, m_context)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_STATUS_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
