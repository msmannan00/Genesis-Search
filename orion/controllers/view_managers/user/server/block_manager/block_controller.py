from django.shortcuts import render

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.view_managers.user.server.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from shared_directory.request_manager.request_handler import request_handler


class block_controller(request_handler):

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
            pass
        else:
            block_controller.__instance = self

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == BLOCK_MODEL_CALLBACK.M_INIT:
            return render(None, CONSTANTS.S_TEMPLATE_NOTICE_WEBSITE_PATH)

