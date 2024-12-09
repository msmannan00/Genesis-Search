import datetime
import json
import math
import time
from trustly.controllers.constants.enums import MONGO_COMMANDS
from trustly.controllers.view_managers.cms.manage_search.class_model.manage_search_model import manage_search_data_model
from trustly.controllers.view_managers.user.interactive.report_manager.class_model.report_data_model import report_data_model
from trustly.controllers.view_managers.user.interactive.sitemap_manager.class_model.sitemap_data_model import sitemap_data_model
from trustly.services.request_manager.request_handler import request_handler
from trustly.services.mongo_manager.mongo_enums import MONGODB_KEYS, MONGODB_COLLECTIONS
from datetime import datetime, timezone


class mongo_request_generator(request_handler):

  def __init__(self):
    pass

  @staticmethod
  def __on_verify_credentials(p_username, p_password):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER: {"m_username": {'$eq': p_username}, "m_password": {'$eq': p_password}}}

  @staticmethod
  def __on_report_url(p_report_data_model: report_data_model):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_REPORT, MONGODB_KEYS.S_VALUE: {"m_url": p_report_data_model.m_url, "m_email": p_report_data_model.m_email, "m_message": p_report_data_model.m_message}}

  @staticmethod
  def __on_upload_url(p_sitemap_data_model: sitemap_data_model):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER: {"m_url": {"$eq": p_sitemap_data_model.m_url}}, MONGODB_KEYS.S_VALUE: {"m_email": p_sitemap_data_model.m_email, "m_name": p_sitemap_data_model.m_name, "m_keyword": p_sitemap_data_model.m_keyword, "m_secret_key": p_sitemap_data_model.m_secret_key, "m_submission_rule": p_sitemap_data_model.m_submission_rule, "m_url": p_sitemap_data_model.m_url}}

  @staticmethod
  def __on_fetch_service_by_url(p_url):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER: {"m_url": p_url}}

  @staticmethod
  def __on_fetch_secret_key(p_secret_key):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_SUBMIT, MONGODB_KEYS.S_FILTER: {'m_secret_key': p_secret_key}}

  @staticmethod
  def __on_update_status(m_name):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_STATUS, MONGODB_KEYS.S_FILTER: {}, MONGODB_KEYS.S_VALUE: {"$set": {m_name: (math.ceil(time.time() / 60))}}}

  @staticmethod
  def __on_fetch_raw(p_data: manage_search_data_model):
    if len(p_data.m_query) < 3:
      p_data.m_query = "{}"
    return {MONGODB_KEYS.S_DOCUMENT: p_data.m_query_collection, MONGODB_KEYS.S_FILTER: json.loads(p_data.m_query)}

  @staticmethod
  def __on_fetch_status():
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_STATUS, MONGODB_KEYS.S_FILTER: {}}

  @staticmethod
  def __on_upload_unique_url(p_url):
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_UNIQUE_URL, MONGODB_KEYS.S_VALUE: {"m_url": p_url}}

  @staticmethod
  def __on_upload_unique_url_clear():
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_UNIQUE_URL, MONGODB_KEYS.S_FILTER: {}, MONGODB_KEYS.S_VALUE: {}}

  @staticmethod
  def __on_upload_unique_url_read():
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_UNIQUE_URL, MONGODB_KEYS.S_FILTER: {}, MONGODB_KEYS.S_VALUE: {}}

  @staticmethod
  def __on_update_url_status(url, url_status=None, leak_status=None, content_type=None):
    update_values = {"url": url}
    utc_now = datetime.now(timezone.utc)
    current_date = utc_now

    if url_status is not None:
      update_values["url_status_date"] = current_date

    if leak_status is not None:
      update_values["leak_status_date"] = current_date

    if content_type is not None:
      update_values["content_type"] = content_type

    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_URL_STATUS, MONGODB_KEYS.S_FILTER: {"url": url}, MONGODB_KEYS.S_VALUE: {"$set": update_values}}

  @staticmethod
  def __on_fetch_url_status():
    return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_URL_STATUS, MONGODB_KEYS.S_FILTER: {}, }

  def invoke_trigger(self, p_commands, p_data=None):
    if p_commands == MONGO_COMMANDS.M_VERIFY_CREDENTIAL:
      return self.__on_verify_credentials(p_data[0], p_data[1])
    if p_commands == MONGO_COMMANDS.M_REPORT_URL:
      return self.__on_report_url(p_data[0])
    if p_commands == MONGO_COMMANDS.M_UPLOAD_URL:
      return self.__on_upload_url(p_data[0])
    if p_commands == MONGO_COMMANDS.M_FIND_URL:
      return self.__on_fetch_service_by_url(p_data)
    if p_commands == MONGO_COMMANDS.M_FIND_SECRET_KEY:
      return self.__on_fetch_secret_key(p_data[0])
    if p_commands == MONGO_COMMANDS.M_FETCH_STATUS:
      return self.__on_fetch_status()
    if p_commands == MONGO_COMMANDS.M_UPDATE_STATUS:
      return self.__on_update_status(p_data[0])
    if p_commands == MONGO_COMMANDS.M_READ_RAW:
      return self.__on_fetch_raw(p_data[0])
    if p_commands == MONGO_COMMANDS.M_UNIQUE_URL_ADD:
      return self.__on_upload_unique_url(p_data[0])
    if p_commands == MONGO_COMMANDS.M_UNIQUE_URL_CLEAR:
      return self.__on_upload_unique_url_clear()
    if p_commands == MONGO_COMMANDS.M_UNIQUE_URL_READ:
      return self.__on_upload_unique_url_read()
    if p_commands == MONGO_COMMANDS.M_CRAWL_HEARTBEAT:
      return self.__on_update_status(p_data[0])
    if p_commands == MONGO_COMMANDS.M_CRONHEARTBEAT:
      return self.__on_update_status(p_data[0])
    if p_commands == MONGO_COMMANDS.M_UPDATE_URL_STATUS:
      return self.__on_update_url_status(p_data[0], p_data[1], p_data[2], p_data[3])
    if p_commands == MONGO_COMMANDS.M_GET_URL_STATUS:
      return self.__on_fetch_url_status()
