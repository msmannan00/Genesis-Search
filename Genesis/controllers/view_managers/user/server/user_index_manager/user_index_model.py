from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.helper_manager.helper_controller import helper_controller
from Genesis.controllers.view_managers.user.server.user_index_manager.user_index_cache_model import user_index_cache_model
from Genesis.controllers.view_managers.user.server.user_index_manager.user_index_enums import USER_INDEX_PARAM, USER_INDEX_CALLBACK, USER_INDEX_MODEL_CALLBACK
from Genesis.controllers.view_managers.user.interactive.notice_manager.notice_session_controller import notice_session_controller
from shared_directory.request_manager.request_handler import request_handler


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
        print("------1",flush=True)
        print(USER_INDEX_PARAM.M_INDEX_BLOCK_URL not in p_data.POST,flush=True)
        print(USER_INDEX_PARAM.M_INDEX_BLOCK_HTML not in p_data.POST,flush=True)
        print(p_data.POST,flush=True)
        print("------1",flush=True)
        if USER_INDEX_PARAM.M_INDEX_BLOCK_URL not in p_data.POST or USER_INDEX_PARAM.M_INDEX_BLOCK_HTML not in p_data.POST:
            return False, None

        print("------2",flush=True)
        m_url = p_data.POST[USER_INDEX_PARAM.M_INDEX_BLOCK_URL]
        print("------3",flush=True)
        m_html = p_data.POST[USER_INDEX_PARAM.M_INDEX_BLOCK_HTML]
        print("------4",flush=True)
        m_host_url = helper_controller.get_host(m_url)
        print("------5",flush=True)

        if helper_controller.is_url_valid(m_url) is False or "#" in m_url is True or len(m_host_url)<5 or m_host_url.__contains__(".onion") is False:
            return False, None
        print("------6",flush=True)

        if m_url not in self.__m_cache:
            print("------7", flush=True)
            self.__m_keys.append(m_url)
            print("------8", flush=True)
            m_data = user_index_cache_model()
            print("------9", flush=True)
            m_data.m_last_epoch = helper_controller.get_seconds_since_epoch()
            print("------10", flush=True)
            m_data.m_hits += 1
            print("------11", flush=True)
            self.__m_cache[m_url] = user_index_cache_model()
            print("------12", flush=True)
            if len(self.__m_keys)>50000:
                print("------13", flush=True)
                self.__m_keys.remove(0)
        else:
            print("------14", flush=True)
            self.__m_keys.remove(m_url)
            print("------15", flush=True)
            self.__m_keys.append(m_url)
            print("------16", flush=True)
            self.__m_cache[m_url].m_hits += 1
        print("------17",flush=True)

        if abs(helper_controller.get_seconds_since_epoch()-self.__m_cache[m_url].m_last_epoch) > 60:
            print("------18----------", flush=True)
            print(m_url, flush=True)
            print("?" in m_url, flush=True)
            print(self.__m_cache[m_url].m_hits>20, flush=True)
            print("?" not in m_url, flush=True)
            print(self.__m_cache[m_url].m_hits>5, flush=True)
            print(helper_controller.normalize_slashes(m_url).endswith(".onion"), flush=True)
            print("------18----------", flush=True)

            if "?" in m_url and self.__m_cache[m_url].m_hits>20 or "?" not in m_url and (self.__m_cache[m_url].m_hits>5 or helper_controller.normalize_slashes(m_url).endswith(".onion")):
                print("------19", flush=True)
                self.__m_cache[m_url].m_hits = 0
                print("------20", flush=True)
                self.__m_cache[m_url].m_last_epoch = helper_controller.get_seconds_since_epoch()
                print("------21", flush=True)
                return True, '{"m_url":"' + m_url + '","m_html":"' + m_html + '"}'

        return False, None

    def __init_page(self, p_data):
        m_status, m_data = self.__service_validator(p_data)
        print("------25", flush=True)
        if m_status:
            print("------26", flush=True)
            self.__save_html(m_data)
            print("------27", flush=True)
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_SUCCESS
        else:
            print("------28", flush=True)
            return USER_INDEX_CALLBACK.M_BLOCK_INDEXED_FAILED

    # External Request Handler
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_INDEX_MODEL_CALLBACK.M_INIT:
            return self.__init_page(p_data)
