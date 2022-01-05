# Local Imports
import base64
import os

from genesis.controllers.constants.constant import APP_STATUS
from genesis.controllers.service_manager.block_manager.block_enums import BLOCK_PARAM, BLOCK_COMMAND
from cryptography.fernet import Fernet

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
        if BLOCK_PARAM.M_SECRET_TOKEN not in p_request.POST and APP_STATUS.S_DEVELOPER is False:
            return False
        else:
            m_secret_token = p_request.POST[BLOCK_PARAM.M_SECRET_TOKEN]
            if self.__m_fernet.decrypt(m_secret_token).startswith(APP_STATUS.S_APP_BLOCK_KEY) is False:
                return False
            return True

    def invoke_trigger(self, p_commands, p_data=None):

        if p_commands == BLOCK_COMMAND.S_VERIFY_REQUEST:
            return self.__on_verify(p_data)
