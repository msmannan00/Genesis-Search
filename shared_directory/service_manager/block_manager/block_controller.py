# Local Imports
import base64
import math
import time

from cryptography.fernet import Fernet

from modules.user_data_parser.parse_services.helper_services.helper_method import helper_method
from shared_directory.service_manager.block_manager.block_enums import BLOCK_PARAM, BLOCK_COMMAND
from shared_directory.service_manager.session.session_controller import session_controller
from shared_directory.service_manager.session.session_enums import SESSION_COMMANDS
from shared_directory.state_manager.constant import APP_STATUS


class block_controller:

    # Local Variables
    __instance = None
    __m_fernet = None

    # Initializations
    @staticmethod
    def getInstance():
        if block_controller.__instance is None:
            block_controller()
        return block_controller.__instance

    def __init__(self):
        block_controller.__instance = self
        self.__m_fernet = Fernet(base64.urlsafe_b64encode(str.encode(APP_STATUS.S_FERNET_KEY)))


    def __on_verify(self, p_request):
        m_status = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS, p_request)
        if m_status is True:
            return False
        try:
            if BLOCK_PARAM.M_SECRET_TOKEN not in p_request.GET and APP_STATUS.S_DEVELOPER is False:
                return True
            elif APP_STATUS.S_DEVELOPER is False:
                m_secret_token = p_request.GET[BLOCK_PARAM.M_SECRET_TOKEN]
                m_decoded_str = self.__m_fernet.decrypt(m_secret_token.encode()).decode("utf-8").split("----")
                m_secret_key = m_decoded_str[0]
                m_secret_time = int(m_decoded_str[1])
                if m_secret_key.startswith(APP_STATUS.S_APP_BLOCK_KEY) is True:
                    m_time = m_secret_time
                    if abs(time.time()-m_time)>86400:
                        return True
                    else:
                        return False
                return True
            return False
        except Exception as ex:
            return True


    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == BLOCK_COMMAND.S_VERIFY_REQUEST:
            return self.__on_verify(p_data)
