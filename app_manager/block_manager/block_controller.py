# Local Imports
import base64
import os
import time
from cryptography.fernet import Fernet
from app_manager.block_manager.block_enums import BLOCK_PARAM, BLOCK_COMMAND
from app_manager.session_manager.session_controller import session_controller
from app_manager.session_manager.session_enums import SESSION_COMMANDS
from app_manager.state_manager.states import APP_STATUS
from dotenv import load_dotenv

load_dotenv()


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
    self.__m_fernet = Fernet(base64.urlsafe_b64encode(str.encode(os.getenv('S_FERNET_KEY'))))

  def __on_verify(self, p_request):
    try:
      if BLOCK_PARAM.M_SECRET_TOKEN not in p_request.GET and APP_STATUS.S_DEVELOPER is False:
        return True
      elif APP_STATUS.S_DEVELOPER is False:
        m_secret_token = p_request.GET[BLOCK_PARAM.M_SECRET_TOKEN]
        m_decoded_str = self.__m_fernet.decrypt(m_secret_token.encode()).decode("utf-8").split("----")
        m_secret_key = m_decoded_str[0]
        m_secret_time = int(m_decoded_str[1])
        if m_secret_key.startswith(os.getenv('S_APP_BLOCK_KEY')) is True:
          m_time = m_secret_time
          if abs(time.time() - m_time) > 129600:
            return True
          else:
            return False
        return True
      return False
    except Exception:
      return True

  def invoke_trigger(self, p_commands, p_data=None):
    if p_commands == BLOCK_COMMAND.S_VERIFY_REQUEST:
      return self.__on_verify(p_data)
