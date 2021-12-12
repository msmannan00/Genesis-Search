from GenesisCrawler.constants.constant import constants
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBControllerEnums import MongoIndexCollection
from GenesisCrawler.controllers.directoryManager.DirectoryControllerEnums import *
from GenesisCrawler.controllers.directoryManager.DirectorySessionController import DirectorySessionController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler

class DirectoryModel(RequestHandler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = DirectorySessionController()
        pass

    def __load_onion_links(self, p_query_model):
        m_services_cursor = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_ONION_LIST, [p_query_model.get_page_number()])
        mRelevanceDocumentList = []

        if m_services_cursor is None:
            return []

        m_counter = 1
        for m_document in m_services_cursor:
            mRelevanceContext = {
                DirectoryModelCallback.M_URL: m_document[MongoIndexCollection.M_URL],
                DirectoryModelCallback.M_CONTENT_TYPE: m_document[MongoIndexCollection.M_CONTENT_TYPE],
                DirectoryModelCallback.M_ID: m_counter + (p_query_model.get_page_number() - 1) * constants.S_SETTINGS_DIRECTORY_LIST_MAX_SIZE,
            }
            mRelevanceDocumentList.append(mRelevanceContext)
            m_counter+=1

        return mRelevanceDocumentList

    def __init_page(self, p_data):
        m_query_model, m_status = self.__m_session.invoke_trigger(DirectorySessionCommands.M_PRE_INIT, [p_data])
        m_query_model.set_query_row_model_list(self.__load_onion_links(m_query_model))
        m_context, m_status = self.__m_session.invoke_trigger(DirectorySessionCommands.M_INIT, [m_query_model])

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DirectoryModelCommands.M_INIT:
            return self.__init_page(p_data)
