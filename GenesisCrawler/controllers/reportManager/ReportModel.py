
from GenesisCrawler.constants import strings
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportModelCommands, ReportCallback, ReportParam, ReportSessionCommands
from GenesisCrawler.controllers.reportManager.ReportSessionController import ReportSessionController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler

class ReportModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = ReportSessionController()
        pass

    def __upload_website(self, p_context):
        m_data = {
            ReportParam.M_URL: p_context[ReportCallback.M_URL],
            ReportParam.M_EMAIL: p_context[ReportCallback.M_EMAIL],
            ReportParam.M_MESSAGE: p_context[ReportCallback.M_MESSAGE],
        }

        MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_REPORT_URL, m_data)

    def __init_page(self, p_data):

        m_context, m_status = self.__m_session.invoke_trigger(ReportSessionCommands.M_INIT, [p_data])
        if m_status is False:
            return m_context, False

        m_context, m_status = self.__m_session.invoke_trigger(ReportSessionCommands.M_VALIDATE, [m_context])
        if m_status is True and strings.S_GENERAL_ONION_DOMAIN in HelperController.getHost(m_context[ReportCallback.M_URL]):
            self.__upload_website(m_context)
            m_context = {}

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ReportModelCommands.M_INIT:
            return self.__init_page(p_data)
