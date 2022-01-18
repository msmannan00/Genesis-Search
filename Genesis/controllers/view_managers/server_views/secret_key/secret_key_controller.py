from django.shortcuts import render

from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.view_managers.server_views.secret_key.secret_key_enums import SECRET_KEY_MODEL_CALLBACK


class secret_key_controller:

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if secret_key_controller.__instance is None:
            secret_key_controller()
        return secret_key_controller.__instance

    def __init__(self):
        if secret_key_controller.__instance is not None:
            pass
        else:
            secret_key_controller.__instance = self

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SECRET_KEY_MODEL_CALLBACK.M_INIT:
            return render(None, CONSTANTS.S_TEMPLATE_SECRET_KEY_WEBSITE_PATH)

