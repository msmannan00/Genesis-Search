from app_manager.log_manager.log_controller import log
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_CALLBACK, DIRECTORY_PARAMS, DIRECTORY_SESSION_COMMANDS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_shared_model.directory_class_model import \
    directory_class_model
from app_manager.request_manager.request_handler import request_handler


class directory_session_controller(request_handler):

    # Helper Methods
    def __pre_init_parameters(self, p_data):
        m_browser = False
        if DIRECTORY_PARAMS.M_PAGE_NUMBER in p_data.GET:
            m_num = int(p_data.GET[DIRECTORY_PARAMS.M_PAGE_NUMBER])
        else:
            m_num = 1

        if m_num<1:
            m_num = 1

        m_directory_model = directory_class_model(m_num, None)

        if DIRECTORY_PARAMS.M_SECURE_SERVICE in p_data.GET:
            m_directory_model.m_site = p_data.GET[DIRECTORY_PARAMS.M_SECURE_SERVICE]

        return m_directory_model, True, m_browser

    def __init_parameters(self, p_links):
        m_context = {
            DIRECTORY_CALLBACK.M_PAGE_NUMBER: p_links.m_page_number,
            DIRECTORY_CALLBACK.M_PAGE_NEXT: p_links.m_page_number+1,
            DIRECTORY_CALLBACK.M_PAGE_BACK: p_links.m_page_number-1,
            DIRECTORY_CALLBACK.M_SECURE_SERVICE_NOTICE: p_links.m_site,
        }

        if len(p_links.m_row_model_list) <= CONSTANTS.S_SETTINGS_DIRECTORY_LIST_MAX_SIZE-2:
            m_context[DIRECTORY_CALLBACK.M_MAX_PAGE_REACHED] = True
        else:
            m_context[DIRECTORY_CALLBACK.M_MAX_PAGE_REACHED] = False

        m_context[DIRECTORY_CALLBACK.M_ONION_LINKS] = p_links.m_row_model_list[0:len(p_links.m_row_model_list)]

        if p_links.m_page_number>1 and len(p_links.m_row_model_list)==0:
            return m_context, False
        else:
            return m_context, True

    def __validate_parameters(self, p_context):
        pass

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_SESSION_COMMANDS.M_PRE_INIT:
            return self.__pre_init_parameters(p_data[0])
        if p_command == DIRECTORY_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])

