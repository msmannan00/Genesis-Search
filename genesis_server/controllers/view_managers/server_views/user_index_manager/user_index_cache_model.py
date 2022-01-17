from genesis_server.controllers.constants.constant import CONSTANTS
from genesis_server.controllers.helper_manager.helper_controller import helper_controller
from genesis_server.controllers.view_managers.user_views.notice_manager.notice_session_controller import notice_session_controller
from genesis_shared_directory.request_manager.request_handler import request_handler
from genesis_server.controllers.view_managers.server_views.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK, USER_INDEX_CALLBACK, USER_INDEX_PARAM


class user_index_cache_model:
    m_last_epoch = 0
    m_hits = 0
