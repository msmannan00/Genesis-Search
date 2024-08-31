import json
import os
import zipfile
import io
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import render
from app_manager.block_manager.block_controller import block_controller
from app_manager.block_manager.block_enums import BLOCK_COMMAND
from app_manager.elastic_manager.elastic_controller import elastic_controller
from trustly import settings
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.server_manager.crawl_index_manager.crawl_enums import CRAWL_COMMANDS, CRAWL_ERROR_CALLBACK
from trustly.controllers.server_manager.crawl_index_manager.crawl_session_controller import crawl_session_controller
from app_manager.request_manager.request_handler import request_handler


class crawl_controller(request_handler):

    # Private Variables
    __instance = None
    __m_session = None

    # Initializations
    @staticmethod
    def getInstance():
        if crawl_controller.__instance is None:
            crawl_controller()
        return crawl_controller.__instance

    def __init__(self):
        if crawl_controller.__instance is not None:
            pass
        else:
            crawl_controller.__instance = self
            self.__m_session = crawl_session_controller()

    def __handle_request(self, p_data):

        m_status, m_crawl_model = self.__m_session.invoke_trigger(CRAWL_COMMANDS.M_INIT, p_data)
        if m_status is False:
            m_context = [False, CRAWL_ERROR_CALLBACK.M_INVALID_PARAM]
            return HttpResponse(json.dumps(m_context))
        else:
            m_response, m_data = elastic_controller.get_instance().invoke_trigger(m_crawl_model.m_command, m_crawl_model.m_data)
            m_context = [m_response, m_data]

            return HttpResponse(json.dumps(m_context))

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        print("::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::")

        if p_command == CRAWL_COMMANDS.M_INIT:
            return self.__handle_request(p_data)
        if p_command == CRAWL_COMMANDS.M_FETCH_FEEDER:
            file_path = os.path.join(settings.BASE_DIR, 'static', 'trustly', '.well-known', 'feeder', "crawl_data.txt")
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="crawl_data.txt")
        if p_command == CRAWL_COMMANDS.M_FETCH_PARSER:
            parser_folder = os.path.join(settings.BASE_DIR, 'static', 'trustly', '.well-known', 'parser')
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_name in os.listdir(parser_folder):
                    file_path = os.path.join(parser_folder, file_name)
                    if os.path.isfile(file_path):
                        zip_file.write(file_path, arcname=os.path.basename(file_name))

            zip_buffer.seek(0)
            return FileResponse(zip_buffer, as_attachment=True, filename='parser_files.zip')