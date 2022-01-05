from django.shortcuts import render
from genesis.controllers.constants.constant import CONSTANTS
from genesis.controllers.view_managers.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from genesis.controllers.view_managers.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK

class block_controller:

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if block_controller.__instance is None:
            block_controller()
        return block_controller.__instance

    def __init__(self):
        if block_controller.__instance is not None:
            raise Exception(BLOCK_MODEL_CALLBACK.ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            block_controller.__instance = self

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == BLOCK_MODEL_CALLBACK.M_INIT:
            return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH)

