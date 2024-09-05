from datetime import datetime, timedelta

from app_manager.elastic_manager.elastic_controller import elastic_controller
from app_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS, ELASTIC_INDEX_COLLECTION
from app_manager.mongo_manager.mongo_controller import mongo_controller
from app_manager.mongo_manager.mongo_enums import MONGODB_CRUD
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.enums import MONGO_COMMANDS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_CALLBACK, DIRECTORY_SESSION_COMMANDS, DIRECTORY_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_session_controller import directory_session_controller
from app_manager.request_manager.request_handler import request_handler


class directory_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = directory_session_controller()
        pass

    from datetime import datetime, timedelta

    def __load_onion_links(self, p_directory_class_model):
        m_documents, m_status = mongo_controller.getInstance().invoke_trigger(
            MONGODB_CRUD.S_READ,
            [
                MONGO_COMMANDS.M_GET_URL_STATUS,
                [],
                [(p_directory_class_model.m_page_number - 1) * 5000, 5000]
            ]
        )

        if m_status:
            m_documents = list(m_documents)

            threshold_date = datetime.utcnow() - timedelta(days=5)

            for mDoc in m_documents:
                if 'leak_status_date' in mDoc:
                    if mDoc['leak_status_date'] < threshold_date:
                        mDoc['leak_status_date'] = 0
                    else:
                        mDoc['leak_status_date'] = 1
                else:
                    mDoc['leak_status_date'] = 0

                if 'url_status_date' in mDoc:
                    if mDoc['url_status_date'] < threshold_date:
                        mDoc['url_status_date'] = 0
                    else:
                        mDoc['url_status_date'] = 1
                else:
                    mDoc['url_status_date'] = 0

            return m_documents
        else:
            return []

    def __init_page(self, p_data):
        m_directory_class_model, m_status, _ = self.__m_session.invoke_trigger(DIRECTORY_SESSION_COMMANDS.M_PRE_INIT, [p_data])
        m_directory_class_model.m_row_model_list  = self.__load_onion_links(m_directory_class_model)
        m_context, m_status = self.__m_session.invoke_trigger(DIRECTORY_SESSION_COMMANDS.M_INIT, [m_directory_class_model])

        return m_context, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_MODEL_COMMANDS.M_INIT:
            return self.__init_page(p_data)
