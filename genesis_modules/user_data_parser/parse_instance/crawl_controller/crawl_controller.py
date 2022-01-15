# Local Imports
import threading

from genesis_modules.user_data_parser.parse_instance.crawl_controller.crawl_enums import CRAWL_CONTROLLER_COMMANDS
from genesis_modules.user_data_parser.parse_instance.i_crawl_crawler.i_crawl_controller import i_crawl_controller
from genesis_modules.user_data_parser.parse_instance.i_crawl_crawler.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from genesis_shared_directory.log_manager.log_controller import log
from genesis_shared_directory.request_manager.request_handler import request_handler


class crawl_controller(request_handler):

    # Crawler Instances & Threads
    __m_main_thread = None
    __m_main_thread_local = None
    __m_crawler_instance_list = []

    # Initializations
    def __init__(self):
        pass

    # Start Crawler Manager

    def __on_run_general(self):
        self.__m_main_thread_local = threading.Thread(target=self.__create_local_crawler_instance, daemon=True)
        self.__m_main_thread_local.start()

    def __create_local_crawler_instance(self):

        # Creating Thread Instace
        m_local_crawler_instance = i_crawl_controller()

        # Saving Thread Instace
        log.g().i("THREAD CREATED : " + str(len(self.__m_crawler_instance_list)))

        # Start Thread Instace
        m_local_crawler_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE, [None])

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER:
            self.__on_run_general()
