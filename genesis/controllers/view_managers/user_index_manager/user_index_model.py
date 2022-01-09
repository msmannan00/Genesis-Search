from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.view_managers.notice_manager.notice_session_controller import notice_session_controller
from genesis.controllers.request_manager.request_handler import request_handler
from genesis.controllers.view_managers.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK, \
    USER_INDEX_CALLBACK, USER_INDEX_PARAM


class user_index_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = notice_session_controller()

    def __save_html(self, p_data):
        text_file = open(CONSTANTS.S_LOCAL_FILE_PATH + "\\" + helper_controller.id_generator() + ".txt", "w")
        text_file.write(p_data)
        text_file.close()

    def __init_page(self, p_data):
        if USER_INDEX_PARAM.M_INDEX_BLOCK in p_data.POST:
            self.__save_html(p_data.POST[USER_INDEX_PARAM.M_INDEX_BLOCK])
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_SUCCESS
        else:
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_FAILED

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_INDEX_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
