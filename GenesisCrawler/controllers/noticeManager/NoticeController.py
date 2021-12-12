from django.http import HttpResponseRedirect
from django.shortcuts import render
from GenesisCrawler.constants.constant import constants
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import NoticeModelCommands
from GenesisCrawler.controllers.noticeManager.NoticeModel import NoticeModel

class NoticeController:

    # Private Variables
    __instance = None
    __m_notice_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if NoticeController.__instance is None:
            NoticeController()
        return NoticeController.__instance

    def __init__(self):
        if NoticeController.__instance is not None:
            raise Exception(NoticeModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            NoticeController.__instance = self
            self.__m_notice_model = NoticeModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == NoticeModelCommands.M_INIT:
            m_response, m_status = self.__m_notice_model.invoke_trigger(NoticeModelCommands.M_INIT, p_data)
            if m_status is True:
                return render(None, constants.S_TEMPLATE_NOTICE_WEBSITE_PATH, m_response)
            else:
                return HttpResponseRedirect(redirect_to="../")

