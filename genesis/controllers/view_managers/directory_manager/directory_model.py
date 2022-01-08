from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.service_manager.elastic_manager.elastic_controller import elastic_controller
from genesis.controllers.service_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS, ELASTIC_INDEX_COLLECTION
from genesis.controllers.view_managers.directory_manager.directory_enums import *
from genesis.controllers.view_managers.directory_manager.directory_session_controller import directory_session_controller
from genesis.controllers.request_manager.request_handler import request_handler

class directory_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = directory_session_controller()
        pass

    def __load_onion_links(self, p_directory_class_model):
        m_documents = elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.S_ONION_LIST,[p_directory_class_model.m_page_number],[None]])
        m_documents = m_documents['hits']['hits']

        mRelevanceDocumentList = []
        if m_documents is None:
            return []

        m_counter = 1
        for m_document in m_documents:
            m_document_item = m_document['_source']
            mRelevanceContext = {
                DIRECTORY_MODEL_CALLBACK.M_URL: m_document_item[ELASTIC_INDEX_COLLECTION.M_HOST],
                DIRECTORY_MODEL_CALLBACK.M_CONTENT_TYPE: m_document_item[ELASTIC_INDEX_COLLECTION.M_CONTENT_TYPE],
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
