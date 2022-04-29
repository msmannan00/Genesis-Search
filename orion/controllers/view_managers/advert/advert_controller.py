
from orion.controllers.view_managers.advert.advert_model import advert_model
from shared_directory.request_manager.request_handler import request_handler


class advert_controller(request_handler):

    # Private Variables
    __instance = None
    __m_advert_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if advert_controller.__instance is None:
            advert_controller()
        return advert_controller.__instance

    def __init__(self):
        if advert_controller.__instance is not None:
            pass
        else:
            advert_controller.__instance = self
            self.__m_advert_model = advert_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        return self.__m_advert_model.invoke_trigger(p_command, p_data)
