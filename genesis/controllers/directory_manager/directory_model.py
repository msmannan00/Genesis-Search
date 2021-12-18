from genesis.constants.constant import CONSTANTS
from genesis.constants.enums import MONGO_COMMANDS
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import mongo_index_collection, MONGODB_CRUD_COMMANDS
from genesis.controllers.directory_manager.directory_enums import *
from genesis.controllers.directory_manager.directory_session_controller import directory_session_controller
from genesis.controllers.shared_model.request_handler import request_handler

class directory_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = directory_session_controller()
        pass

    def __load_onion_links(self, p_directory_class_model):
        m_services_cursor = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_READ, [MONGO_COMMANDS.M_ONION_LIST, p_directory_class_model.m_page_number])
        mRelevanceDocumentList = []

        if m_services_cursor is None:
            return []

        m_counter = 1
        for m_document in m_services_cursor:
            mRelevanceContext = {
                DIRECTORY_MODEL_CALLBACK.M_URL: m_document[mongo_index_collection.M_URL],
                DIRECTORY_MODEL_CALLBACK.M_CONTENT_TYPE: m_document[mongo_index_collection.M_CONTENT_TYPE],
                DIRECTORY_MODEL_CALLBACK.M_ID: m_counter + (p_directory_class_model.m_page_number - 1) * CONSTANTS.S_SETTINGS_DIRECTORY_LIST_MAX_SIZE,
            }
            mRelevanceDocumentList.append(mRelevanceContext)
            m_counter+=1

        return mRelevanceDocumentList

    def __init_page(self, p_data):
        m_directory_class_model, m_status = self.__m_session.invoke_trigger(DIRECTORY_SESSION_COMMANDS.M_PRE_INIT, [p_data])
        m_directory_class_model.m_row_model_list  = self.__load_onion_links(m_directory_class_model)
        m_context, m_status = self.__m_session.invoke_trigger(DIRECTORY_SESSION_COMMANDS.M_INIT, [m_directory_class_model])

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
