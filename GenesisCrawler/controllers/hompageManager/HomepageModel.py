from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageModelCommands, HomepageSessionCommands
from GenesisCrawler.controllers.hompageManager.HomepageSessionController import HomepageSessionController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class HomepageModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = HomepageSessionController()
        pass

    def __init_page(self):
        m_context, m_status = self.__m_session.invoke_trigger(HomepageSessionCommands.M_INIT, None)

        return m_context, m_status

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == HomepageModelCommands.M_INIT:
            return self.__init_page()
