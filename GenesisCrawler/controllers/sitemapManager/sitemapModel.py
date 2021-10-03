
from GenesisCrawler.constants import strings
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.message import *
from GenesisCrawler.constants.strings import S_DEFAULT_SUBMISSION_RULE_1, S_DEFAULT_SUBMISSION_RULE_2
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler
from GenesisCrawler.controllers.sitemapManager.SitemapSessionController import SitemapSessionController
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapModelCommands, SitemapCallback, \
    SitemapParam, SitemapSessionCommands


class SitemapModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = SitemapSessionController()

    def __upload__website(self, p_context):
        m_data = {
            SitemapParam.M_URL: p_context[SitemapCallback.M_URL],
            SitemapParam.M_EMAIL: p_context[SitemapCallback.M_EMAIL],
            SitemapParam.M_NAME: p_context[SitemapCallback.M_NAME],
            SitemapParam.M_KEYWORD: p_context[SitemapCallback.M_KEYWORD],
            SitemapParam.M_SECRETKEY: p_context[SitemapCallback.M_SECRETKEY],
            SitemapParam.M_URL.M_SUBMISSION_RULES: p_context[SitemapCallback.M_SUBMISSION_RULES],
        }

        MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_UPLOAD_URL, m_data)

    def __init_page(self, p_data):
        m_context, m_status = self.__m_session.invoke_trigger(SitemapSessionCommands.M_INIT, [p_data])
        if m_status is False:
            return m_context, False

        m_context, m_status = self.__m_session.invoke_trigger(SitemapSessionCommands.M_VALIDATE, [m_context])
        if m_status is True and strings.S_GENERAL_ONION_DOMAIN in HelperController.getHost(m_context[SitemapCallback.M_URL]):
            self.__upload__website(m_context)

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SitemapModelCommands.M_INIT:
            return self.__init_page(p_data)
