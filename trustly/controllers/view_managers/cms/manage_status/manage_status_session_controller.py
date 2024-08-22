import datetime
import math
import time

from app_manager.session_manager.session_controller import session_controller
from trustly.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_SESSION_COMMANDS, MANAGE_STATUS_CALLBACK
from app_manager.request_manager.request_handler import request_handler
from app_manager.session_manager.session_enums import SESSION_KEYS, SESSION_COMMANDS


class manage_status_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        m_status = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS, p_data)
        if SESSION_KEYS.S_USERNAME in p_data.session :
            return {}, m_status
        else :
            return {}, m_status

    def __validate_parameters(self, p_data):
        m_current_time = math.ceil(time.time()/60)
        m_cronjob_time = p_data['m_cronjob']
        m_crawler_time = p_data['m_crawler']

        if (m_current_time - int(m_crawler_time))>10:
            m_crawler_notice = "not running"
        elif (m_current_time - int(m_crawler_time))>5:
            m_crawler_notice = "un-responsive"
        else:
            m_crawler_notice = "running"

        if (m_current_time - int(m_cronjob_time))>10:
            m_cronjob_notice = "not running"
        elif (m_current_time - int(m_cronjob_time))>5:
            m_cronjob_notice = "un-responsive"
        else:
            m_cronjob_notice = "running"

        m_cronjob_time = datetime.datetime.fromtimestamp(m_cronjob_time*60).strftime('%Y-%m-%d %H:%M')
        m_crawler_time = datetime.datetime.fromtimestamp(m_crawler_time*60).strftime('%Y-%m-%d %H:%M')

        m_context_response = {
            MANAGE_STATUS_CALLBACK.M_CRONJOB_NOTICE : m_cronjob_notice,
            MANAGE_STATUS_CALLBACK.M_CRONJOB_TIME : m_cronjob_time,
            MANAGE_STATUS_CALLBACK.M_CRAWLER_NOTICE : m_crawler_notice,
            MANAGE_STATUS_CALLBACK.M_CRAWLER_TIME : m_crawler_time
        }

        return m_context_response


    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_STATUS_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)
        if p_command == MANAGE_STATUS_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data)

