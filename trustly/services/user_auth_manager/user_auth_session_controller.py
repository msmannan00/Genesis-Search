from trustly.services.user_auth_manager.class_model.user_model import user_model
from trustly.services.user_auth_manager.user_auth_enums import USER_AUTH_COMMANDS, USER_AUTH_PARAM
from trustly.services.request_manager.request_handler import request_handler


class user_auth_session_controller(request_handler):

  # Helper Methods
  @staticmethod
  def __init_parameters(p_data):
    m_user_model = user_model()

    if USER_AUTH_PARAM.M_USERNAME in p_data.POST:
      m_user_model.m_username = p_data.POST[USER_AUTH_PARAM.M_USERNAME]
    if USER_AUTH_PARAM.M_PASSWORD in p_data.POST:
      m_user_model.m_password = p_data.POST[USER_AUTH_PARAM.M_PASSWORD]

    return m_user_model

  # External Request Callbacks
  def invoke_trigger(self, p_command, p_data):
    if p_command == USER_AUTH_COMMANDS.M_INIT:
      return self.__init_parameters(p_data)
