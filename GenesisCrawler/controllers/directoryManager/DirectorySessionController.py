from GenesisCrawler.constants.constants import constants
from GenesisCrawler.controllers.directoryManager.DirectoryControllerEnums import DirectoryParam, DirectoryCallback, DirectorySessionCommands
from GenesisCrawler.controllers.directoryManager.directoryModel.queryModel import QueryModel
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class DirectorySessionController(RequestHandler):

    # Helper Methods
    def __pre_init_parameters(self, p_data):
        if DirectoryParam.M_PAGE_NUMBER in p_data.POST:
            m_num = int(p_data.POST[DirectoryParam.M_PAGE_NUMBER])
        else:
            m_num = 1

        if DirectoryParam.M_PAGE_NUMBER_NEXT in p_data.POST:
            m_num+=1
        elif DirectoryParam.M_PAGE_NUMBER_PREV in p_data.POST:
            m_num-=1

        m_query_model = QueryModel(m_num, None)
        return m_query_model, True

    def __init_parameters(self, p_links):
        m_context = {
            DirectoryCallback.M_PAGE_NUMBER: p_links.get_page_number(),
        }

        if len(p_links.get_query_row_model_list()) <= constants.S_SETTINGS_DIRECTORY_LIST_MAX_SIZE:
            m_context[DirectoryCallback.M_MAX_PAGE_REACHED] = True
        else:
            m_context[DirectoryCallback.M_MAX_PAGE_REACHED] = False

        if len(p_links.get_query_row_model_list()) > 1:
            m_context[DirectoryCallback.M_ONION_LINKS] = p_links.get_query_row_model_list()[0:len(p_links.get_query_row_model_list()) - 1]
        else:
            m_context[DirectoryCallback.M_ONION_LINKS] = p_links.get_query_row_model_list()[0:len(p_links.get_query_row_model_list())]

        return m_context, True

    def __validate_parameters(self, p_context):
        pass

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DirectorySessionCommands.M_PRE_INIT:
            return self.__pre_init_parameters(p_data[0])
        if p_command == DirectorySessionCommands.M_INIT:
            return self.__init_parameters(p_data[0])

