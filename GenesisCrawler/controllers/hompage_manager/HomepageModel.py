from GenesisCrawler.controllers.hompage_manager.HomepageEnums import HOMEPAGE_MODEL_COMMANDS, HOMEPAGE_SESSION_COMMANDS
from GenesisCrawler.controllers.hompage_manager.HomepageSessionController import HomepageSessionController
from GenesisCrawler.controllers.shared_model.request_handler import request_handler


class HomepageModel(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = HomepageSessionController()
        pass

    def __init_page(self):
        m_context, m_status = self.__m_session.invoke_trigger(HOMEPAGE_SESSION_COMMANDS.M_INIT, None)

        return m_context, m_status

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_MODEL_COMMANDS.M_INIT:
            return self.__init_page()
