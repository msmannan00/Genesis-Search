
from django.shortcuts import render
from GenesisCrawler.constants.constant import CONSTANTS
from GenesisCrawler.controllers.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from GenesisCrawler.controllers.directory_manager.directory_model import directory_model
from GenesisCrawler.controllers.shared_model.request_handler import request_handler


class directory_controller(request_handler):

    # Private Variables
    __instance = None
    __m_directory_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if directory_controller.__instance is None:
            directory_controller()
        return directory_controller.__instance

    def __init__(self):
        if directory_controller.__instance is not None:
            raise Exception(DIRECTORY_MODEL_COMMANDS.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            directory_controller.__instance = self
            self.__m_directory_model = directory_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DIRECTORY_MODEL_COMMANDS.M_INIT:
            m_response, m_status = self.__m_directory_model.invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, p_data)
            if m_status is not True:
                return render(None, CONSTANTS.S_TEMPLATE_INDEX_PATH, m_response)
            else:
                return render(None, CONSTANTS.S_TEMPLATE_DIRECTORY_WEBSITE_PATH, m_response)
        else:
            m_response = None
        return m_response

