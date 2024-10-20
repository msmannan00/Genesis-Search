from django.http import HttpResponse

from orion.controllers.view_managers.user.server.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK
from orion.controllers.view_managers.user.server.user_index_manager.user_index_model import user_index_model
from shared_directory.request_manager.request_handler import request_handler


class user_index_controller(request_handler):

    # Private Variables
    __instance = None
    __m_user_index_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if user_index_controller.__instance is None:
            user_index_controller()
        return user_index_controller.__instance

    def __init__(self):
        if user_index_controller.__instance is not None:
            pass
        else:
            user_index_controller.__instance = self
            self.__m_user_index_model = user_index_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == USER_INDEX_MODEL_CALLBACK.M_INIT:
            return HttpResponse(self.__m_user_index_model.invoke_trigger(USER_INDEX_MODEL_CALLBACK.M_INIT, p_data))



