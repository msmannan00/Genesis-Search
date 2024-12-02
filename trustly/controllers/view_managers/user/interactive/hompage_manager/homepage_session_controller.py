import ast
import json

from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.helper_manager.helper_controller import helper_controller
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_CALLBACK, HOMEPAGE_PARAM, HOMEPAGE_SESSION_COMMANDS
from trustly.services.redis_manager.redis_controller import redis_controller
from trustly.services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_KEYS, REDIS_DEFAULT
from trustly.services.request_manager.request_handler import request_handler

class homepage_session_controller(request_handler):

    @staticmethod
    def __init_parameters(p_data):
        results_dict = redis_controller().invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [REDIS_KEYS.INSIGHT_STAT, REDIS_DEFAULT.INSIGHT_STAT_DEFAULT, None])
        results_dict = ast.literal_eval(results_dict)

        m_context = {
            HOMEPAGE_CALLBACK.M_REFERENCE: helper_controller.load_json(CONSTANTS.S_REFERENCE_WEBSITE_URL),
            HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE: GENERAL_STRINGS.S_GENERAL_HTTP,
            HOMEPAGE_CALLBACK.M_STATISTICS: results_dict
        }

        if HOMEPAGE_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_context[HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE] = p_data.GET[HOMEPAGE_PARAM.M_SECURE_SERVICE]

        return m_context, True

    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)
