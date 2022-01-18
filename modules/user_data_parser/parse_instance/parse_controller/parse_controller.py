import warnings

from modules.user_data_parser.parse_instance.parse_controller.parse_enums import PARSE_COMMANDS
from modules.user_data_parser.parse_instance.constants.strings import ERROR_MESSAGES
from modules.user_data_parser.parse_instance.crawl_controller.crawl_controller import crawl_controller
from modules.user_data_parser.parse_instance.crawl_controller.crawl_enums import CRAWL_CONTROLLER_COMMANDS
from shared_directory.request_manager.request_handler import request_handler

warnings.filterwarnings("ignore", category=DeprecationWarning)

class parse_controller(request_handler):
    __instance = None
    __m_crawl_controller = None

    # Initializations
    @staticmethod
    def get_instance():
        if parse_controller.__instance is None:
            parse_controller()
        return parse_controller.__instance

    def __init__(self):
        if parse_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            self.__m_crawl_controller = crawl_controller()
            parse_controller.__instance = self

    # External Reuqest Callbacks
    def __on_start(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER)

    # External Reuqest Manager
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == PARSE_COMMANDS.S_START_PARSER:
            return self.__on_start()
