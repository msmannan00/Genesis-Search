from django.shortcuts import render
from genesis_server.controllers.constants.constant import CONSTANTS
from genesis_server.controllers.view_managers.server_views.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK
from genesis_shared_directory.service_manager.block_manager.block_controller import block_controller
from genesis_shared_directory.service_manager.block_manager.block_enums import BLOCK_COMMAND


class maintenance_controller:

    # Private Variables
    __instance = None

    # Initializations
    @staticmethod
    def getInstance():
        if maintenance_controller.__instance is None:
            maintenance_controller()
        return maintenance_controller.__instance

    def __init__(self):
        if maintenance_controller.__instance is not None:
            pass
        else:
            maintenance_controller.__instance = self

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == MAINTENANCE_MODEL_CALLBACK.M_INIT:
            return render(None, CONSTANTS.S_TEMPLATE_MAINTENANCE_WEBSITE_PATH)

