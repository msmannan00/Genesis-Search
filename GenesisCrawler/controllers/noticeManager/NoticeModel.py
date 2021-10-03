from GenesisCrawler.constants import strings
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import *
from GenesisCrawler.controllers.noticeManager.NoticeSessionController import NoticeSessionController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class NoticeModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = NoticeSessionController()

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(NoticeSessionCommands.M_INIT, [p_data])

        return m_context, m_status

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == NoticeModelCommands.M_INIT:
            return self.__init_page(p_data)
