from django.shortcuts import render
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.view_managers.user.interactive.policy_manager.policy_enums import POLICY_MODEL_CALLBACK
from trustly.services.request_manager.request_handler import request_handler


class policy_view_model(request_handler):

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if policy_view_model.__instance is None:
            policy_view_model()
        return policy_view_model.__instance

    def __init__(self):
        if policy_view_model.__instance is not None:
            pass
        else:
            policy_view_model.__instance = self

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == POLICY_MODEL_CALLBACK.M_INIT:
            return render(None, CONSTANTS.S_TEMPLATE_POLICY_WEBSITE_PATH)

