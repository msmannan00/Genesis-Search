import os
import random

from django.http import HttpResponseRedirect, HttpResponse

from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.constants.enums import MONGO_COMMANDS
from orion.controllers.constants.strings import GENERAL_STRINGS
from orion.controllers.helper_manager.helper_controller import helper_controller
from orion.controllers.view_managers.advert.advert_enums import ADVERT_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.report_manager.report_enums import REPORT_SESSION_COMMANDS, REPORT_CALLBACK
from orion.controllers.view_managers.user.interactive.report_manager.report_session_controller import report_session_controller
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.mongo_manager.mongo_controller import mongo_controller
from shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD


class advert_model(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    def __init__(self):
        self.__m_session = report_session_controller()
        pass

    def __fetch_advert(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_data = open(dir_path+"/sample_advert/" + str(random.randint(1, 5)) + ".png", "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg")

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == ADVERT_MODEL_COMMANDS.M_FETCH_ADVERT:
            return self.__fetch_advert()
