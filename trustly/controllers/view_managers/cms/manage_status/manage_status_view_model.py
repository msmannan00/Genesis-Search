from trustly.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.manage_status.manage_status_model import manage_status_model


class manage_status_view_model:
  # Private Variables
  __instance = None
  __m_manage_status_model = None

  # Initializations
  @staticmethod
  def getInstance():
    if manage_status_view_model.__instance is None:
      manage_status_view_model()
    return manage_status_view_model.__instance

  def __init__(self):
    if manage_status_view_model.__instance is not None:
      pass
    else:
      manage_status_view_model.__instance = self
      self.__m_manage_status_model = manage_status_model()

  # External Request Callbacks
  def invoke_trigger(self, p_command, p_data):
    if p_command == MANAGE_STATUS_MODEL_CALLBACK.M_INIT:
      m_redirection = self.__m_manage_status_model.invoke_trigger(MANAGE_STATUS_MODEL_CALLBACK.M_INIT, p_data)
      return m_redirection
