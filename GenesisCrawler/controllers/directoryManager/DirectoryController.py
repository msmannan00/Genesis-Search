
from django.shortcuts import render
from GenesisCrawler.constants.constant import constants
from GenesisCrawler.controllers.directoryManager.DirectoryControllerEnums import DirectoryModelCommands
from GenesisCrawler.controllers.directoryManager.DirectoryModel import DirectoryModel
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class DirectoryController(RequestHandler):

    # Private Variables
    __instance = None
    __m_directory_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if DirectoryController.__instance is None:
            DirectoryController()
        return DirectoryController.__instance

    def __init__(self):
        if DirectoryController.__instance is not None:
            raise Exception(DirectoryModelCommands.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            DirectoryController.__instance = self
            self.__m_directory_model = DirectoryModel()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DirectoryModelCommands.M_INIT:
            m_response, m_status = self.__m_directory_model.invoke_trigger(DirectoryModelCommands.M_INIT, p_data)
            if m_status is not True:
                return render(None, constants.S_TEMPLATE_INDEX_PATH, m_response)
            else:
                return render(None, constants.S_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
        else:
            m_response = None
        return m_response

