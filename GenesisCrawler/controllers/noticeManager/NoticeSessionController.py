from GenesisCrawler.constants import strings
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import NoticeCallback, NoticeParam, \
    NoticeSessionCommands
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class NoticeSessionController(RequestHandler):

    # Helper Methods
    def __init_parameters(self, p_data):
        # Local Variables
        m_status = False

        # Default Initialization
        m_context = {
            NoticeCallback.M_TYPE: strings.S_GENERAL_EMPTY,
            NoticeCallback.M_DATA: strings.S_GENERAL_EMPTY,
        }

        # Notice Header Param
        if NoticeParam.M_HEADER in p_data.GET:
            m_context[NoticeCallback.M_TYPE] = p_data.GET[NoticeParam.M_HEADER]
            m_status = True

        # Notice Data Param
        if NoticeParam.M_DATA in p_data.GET:
            m_context[NoticeCallback.M_DATA] = p_data.GET[NoticeParam.M_DATA]

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NoticeSessionCommands.M_INIT:
            return self.__init_parameters(p_data[0])

