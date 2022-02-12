# Local Imports
import json
import os
import threading

from abc import ABC
from time import sleep
from django.utils.text import unescape_entities
from modules.user_data_parser.parse_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS, RAW_PATH_CONSTANTS
from modules.user_data_parser.parse_instance.constants.strings import MESSAGE_STRINGS, STRINGS
from modules.user_data_parser.parse_instance.i_crawl_crawler.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from modules.user_data_parser.parse_instance.i_crawl_crawler.static_parse_controller import static_parse_controller
from modules.user_data_parser.parse_instance.local_shared_model.url_model import url_model
from modules.user_data_parser.parse_services.helper_services.helper_method import helper_method
from shared_directory.log_manager.log_controller import log
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.elastic_manager.elastic_controller import elastic_controller
from shared_directory.service_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, \
    ELASTIC_REQUEST_COMMANDS


class i_crawl_controller(request_handler, ABC):

    __m_parsed_model = None

    def __init__(self):
        pass

    def __clean_sub_url(self, p_parsed_model):
        m_sub_url_filtered = []
        for m_sub_url in  p_parsed_model.m_sub_url:
            if m_sub_url not in m_sub_url_filtered:
                m_sub_url_filtered.append(m_sub_url)
        p_parsed_model.m_sub_url = m_sub_url_filtered


        return p_parsed_model

    # Web Request To Get Physical URL HTML
    def __trigger_url_request(self, p_request_model, p_html):
        m_html_parser = static_parse_controller()
        m_status, m_parsed_model = m_html_parser.on_parse_html(p_html, p_request_model)

        if 1==1 or m_status is False and m_parsed_model.m_validity_score >= 15 and (len(m_parsed_model.m_content) > 0):
            m_parsed_model = self.__clean_sub_url(m_parsed_model)
            m_parsed_model.m_user_crawled = True
            elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_UPDATE, [ELASTIC_REQUEST_COMMANDS.S_INDEX_USER_QUERY, [m_parsed_model], [True]])
            log.g().s( MESSAGE_STRINGS.S_LOCAL_URL_PARSED + STRINGS.S_SEPERATOR + m_parsed_model.m_base_url_model.m_url + " : " + str( threading.get_native_id()))
        else:
            log.g().w(MESSAGE_STRINGS.S_LOW_YIELD_URL + " : " + p_request_model.m_url)

        return None

    def __find_recent_file(self):
        try:
            os.makedirs(RAW_PATH_CONSTANTS.S_LOCAL_FILE_PATH)
        except OSError:
            pass

        m_doc_list = sorted([RAW_PATH_CONSTANTS.S_LOCAL_FILE_PATH + "/" + f for f in os.listdir(RAW_PATH_CONSTANTS.S_LOCAL_FILE_PATH)], key=os.path.getctime)
        if len(m_doc_list)>1:
            m_file = m_doc_list[0]
            m_json = open(m_file, "rb").read()
            os.remove(m_file)
            m_data = json.loads(m_json, strict=False)
            m_url = helper_method.on_clean_url(helper_method.normalize_slashes(m_data['m_url'] + "////"))
            return True, url_model(m_url,0,'g'),  unescape_entities(m_data['m_html'])
        else:
            return False, None, None

    # Crawl Manager Awakes Crawler Instance From Sleep
    def __start_crawler_instance(self):
        while True:
            try:
               sleep(CRAWL_SETTINGS_CONSTANTS.S_LOCAL_FILE_CRAWLER_INVOKE_DELAY)
               m_status, m_url_model, m_html = self.__find_recent_file()
               if m_status is False:
                   log.g().w(MESSAGE_STRINGS.S_LOCAL_URL_EMPTY)
                   sleep(CRAWL_SETTINGS_CONSTANTS.S_LOCAL_FILE_CRAWLER_INVOKE_DELAY_LONG)
               else:
                   self.__trigger_url_request(m_url_model, m_html)
            except Exception as ex:
                log.g().e("ICRAWL LOCAL ERROR E1 : " + str(ex))


    def invoke_trigger(self, p_command, p_data=None):
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE:
            self.__start_crawler_instance()
