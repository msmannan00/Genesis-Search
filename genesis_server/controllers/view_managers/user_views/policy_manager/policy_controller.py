from django.shortcuts import render
from genesis_server.controllers.constants.constant import CONSTANTS
from genesis_shared_directory.service_manager.block_manager.block_controller import block_controller
from genesis_shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND
from genesis_server.controllers.view_managers.user_views.policy_manager.policy_enums import POLICY_MODEL_CALLBACK
from genesis_shared_directory.state_manager.server_vars import SERVER_VARS


class policy_controller:

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if policy_controller.__instance is None:
            policy_controller()
        return policy_controller.__instance

    def __init__(self):
        if policy_controller.__instance is not None:
            pass
        else:
            policy_controller.__instance = self

    def __on_verify_app(self, p_data):
        return block_controller.getInstance().invoke_trigger(BLOCK_COMMAND.S_VERIFY_REQUEST, p_data)

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == POLICY_MODEL_CALLBACK.M_INIT:
            if self.__on_verify_app(p_data) is True:
                return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)
            elif SERVER_VARS.S_MAINTAINANCE is True:
                return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)
            else:
                return render(None, CONSTANTS.S_TEMPLATE_POLICY_WEBSITE_PATH)

