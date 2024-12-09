from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_model import notice_model
from trustly.services.request_manager.request_handler import request_handler
from trustly.controllers.view_managers.user.server.error.error_view_model import error_view_model
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK


class notice_view_model(request_handler):
  # Private Variables
  __instance = None
  __m_notice_model = None

  # Initializations
  @staticmethod
  def getInstance():
    if notice_view_model.__instance is None:
      notice_view_model()
    return notice_view_model.__instance

  def __init__(self):
    if notice_view_model.__instance is not None:
      pass
    else:
      notice_view_model.__instance = self
      self.__m_notice_model = notice_model()

  # External Request Callbacks
  def invoke_trigger(self, p_command, p_data):
    if p_command == NOTICE_MODEL_CALLBACK.M_INIT:
      m_response, m_status, m_browser = self.__m_notice_model.invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, p_data)
      if m_status is True:
        return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH, m_response)
      else:
        return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [p_data, 404])
