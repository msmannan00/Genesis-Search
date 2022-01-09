from django.http import HttpResponseRedirect
from django.shortcuts import render
from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.service_manager.block_manager.block_controller import block_controller
from genesis.controllers.service_manager.block_manager.block_enums import BLOCK_COMMAND
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
            pass
        else:
            notice_controller.__instance = self
            self.__m_notice_model = notice_model()

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NOTICE_MODEL_CALLBACK.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)

            m_response, m_status = self.__m_notice_model.invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, p_data)
            if m_status is True:
                return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to="../")

