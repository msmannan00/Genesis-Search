from django.http import HttpResponseRedirect
from django.shortcuts import render
from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.view_managers.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from genesis.controllers.view_managers.notice_manager.notice_model import notice_model

class notice_controller:

    # Private Variables
    __instance = None
    __m_notice_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if notice_controller.__instance is None:
            notice_controller()
        return notice_controller.__instance

    def __init__(self):
        if notice_controller.__instance is not None:
            raise Exception(NOTICE_MODEL_CALLBACK.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            notice_controller.__instance = self
            self.__m_notice_model = notice_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NOTICE_MODEL_CALLBACK.M_INIT:
            m_response, m_status = self.__m_notice_model.invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, p_data)
            if m_status is True:
                return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to="../")

