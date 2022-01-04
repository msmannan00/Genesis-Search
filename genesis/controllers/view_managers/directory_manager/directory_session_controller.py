from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.view_managers.directory_manager.directory_enums import DIRECTORY_PARAMS, DIRECTORY_CALLBACK, DIRECTORY_SESSION_COMMANDS
from genesis.controllers.view_managers.directory_manager.directory_shared_model.directory_class_model import directory_class_model
from genesis.controllers.request_manager.request_handler import request_handler


class directory_session_controller(request_handler):

    # Helper Methods
    def __pre_init_parameters(self, p_data):
        if DIRECTORY_PARAMS.M_PAGE_NUMBER in p_data.POST:
            m_num = int(p_data.POST[DIRECTORY_PARAMS.M_PAGE_NUMBER])
        else:
            m_num = 1

        if DIRECTORY_PARAMS.M_PAGE_NUMBER_NEXT in p_data.POST:
            m_num+=1
        elif DIRECTORY_PARAMS.M_PAGE_NUMBER_PREV in p_data.POST:
            m_num-=1

        m_directory_model = directory_class_model(m_num, None)
        return m_directory_model, True

    def __init_parameters(self, p_links):
        m_context = {
            DIRECTORY_CALLBACK.M_PAGE_NUMBER: p_links.m_page_number,
        }

        if len(p_links.m_row_model_list) <= CONSTANTS.S_SETTINGS_DIRECTORY_LIST_MAX_SIZE:
            m_context[DIRECTORY_CALLBACK.M_MAX_PAGE_REACHED] = True
        else:
            m_context[DIRECTORY_CALLBACK.M_MAX_PAGE_REACHED] = False

        if len(p_links.m_row_model_list) > 1:
            m_context[DIRECTORY_CALLBACK.M_ONION_LINKS] = p_links.m_row_model_list[0:len(p_links.m_row_model_list) - 1]
        else:
            m_context[DIRECTORY_CALLBACK.M_ONION_LINKS] = p_links.m_row_model_list[0:len(p_links.m_row_model_list)]

        return m_context, True

    def __validate_parameters(self, p_context):
        pass

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_SESSION_COMMANDS.M_PRE_INIT:
            return self.__pre_init_parameters(p_data[0])
        if p_command == DIRECTORY_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])

