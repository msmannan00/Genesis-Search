from genesis_server.controllers.constants.constant import CONSTANTS
from genesis_server.controllers.helper_manager.helper_controller import helper_controller
from genesis_server.controllers.view_managers.server_views.user_index_manager.user_index_cache_model import \
    user_index_cache_model
from genesis_server.controllers.view_managers.user_views.notice_manager.notice_session_controller import notice_session_controller
from genesis_shared_directory.request_manager.request_handler import request_handler
from genesis_server.controllers.view_managers.server_views.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK, USER_INDEX_CALLBACK, USER_INDEX_PARAM


class user_index_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None
    __m_keys = []
    __m_cache = {}

    # Initializations
    def __init__(self):
        self.__m_session = notice_session_controller()

    def __save_html(self, p_data):
        text_file = open(CONSTANTS.S_LOCAL_FILE_PATH + "/" + helper_controller.id_generator() + ".txt", "w")
        text_file.write(p_data)
        text_file.close()

    def __service_validator(self, p_data):
        if USER_INDEX_PARAM.M_INDEX_BLOCK_URL not in p_data.POST or USER_INDEX_PARAM.M_INDEX_BLOCK_HTML not in p_data.POST:
            return False, None

        m_url = p_data.POST[USER_INDEX_PARAM.M_INDEX_BLOCK_URL]
        m_html = p_data.POST[USER_INDEX_PARAM.M_INDEX_BLOCK_HTML]
        m_host_url = helper_controller.get_host(m_url)

        if helper_controller.is_url_valid(m_url) is False or "#" in m_url is True or len(m_host_url)<5 or m_host_url.__contains__(".onion") is False:
            return False, None

        if m_url not in self.__m_cache:
            self.__m_keys.append(m_url)
            m_data = user_index_cache_model()
            m_data.m_last_epoch = helper_controller.get_seconds_since_epoch()
            m_data.m_hits += 1
            self.__m_cache[m_url] = user_index_cache_model()
            if len(self.__m_keys)>50000:
                self.__m_keys.remove(0)
        else:
            self.__m_keys.remove(m_url)
            self.__m_keys.append(m_url)
            self.__m_cache[m_url].m_hits += 1

        if abs(helper_controller.get_seconds_since_epoch()-self.__m_cache[m_url].m_last_epoch) > 60:
            if "?" in m_url and self.__m_cache[m_url].m_hits>20 or "?" not in m_url and (self.__m_cache[m_url].m_hits>5 or helper_controller.normalize_slashes(m_url).endswith(".onion")):
                self.__m_cache[m_url].m_hits = 0
                self.__m_cache[m_url].m_last_epoch = helper_controller.get_seconds_since_epoch()
                return True, '{"m_url":"' + m_url + '","m_html":"' + m_html + '"}'

        return False, None

    def __init_page(self, p_data):
        m_status, m_data = self.__service_validator(p_data)
        if m_status:
            self.__save_html(m_data)
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_SUCCESS
        else:
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_FAILED

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_INDEX_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
