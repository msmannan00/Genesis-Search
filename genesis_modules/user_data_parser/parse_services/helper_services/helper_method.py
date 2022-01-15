# Local Imports
import datetime
import math
import os
import time
from typing import re
from urllib.parse import urlparse

import requests
import urllib3
from gensim.parsing.preprocessing import STOPWORDS


class helper_method:

    # Base URL Verify - In case if url is non parsable image
    @staticmethod
    def is_url_base_64(p_url):
        if str(p_url).startswith("duplicationHandlerService:"):
            return True
        else:
            return False

    @staticmethod
    def clean_description(p_data):
        return re.sub(r'[^a-zA-Z0-9. ,-]', '', p_data)

    # Extract URL Host
    @staticmethod
    def get_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]
        return m_host_url

    @staticmethod
    def split_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]
        return m_host_url, p_url[len(m_host_url):]

    # URL Cleaner
    @staticmethod
    def on_clean_url(p_url):
        if p_url.startswith("http://www.") or p_url.startswith("https://www.") or p_url.startswith("www."):
            p_url = p_url.replace("www.", "", 1)

        while p_url.endswith("/") or p_url.endswith(" "):
            p_url = p_url[:-1]

        return p_url

    # Remove Extra Slashes
    @staticmethod
    def normalize_slashes(p_url):
        p_url = str(p_url)
        segments = p_url.split('/')
        correct_segments = []
        for segment in segments:
            if segment != '':
                correct_segments.append(segment)
        normalized_url = '/'.join(correct_segments)
        normalized_url = normalized_url.replace("http:/","http://")
        normalized_url = normalized_url.replace("https:/","https://")
        normalized_url = normalized_url.replace("ftp:/","ftp://")
        return normalized_url

    @staticmethod
    def on_create_session():
        m_request_handler = requests.Session()
        m_request_handler.max_redirects = 5
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        return m_request_handler

    @staticmethod
    def get_mongodb_date():
        return datetime.datetime.utcnow()

    @staticmethod
    def is_stop_word(p_word):
        if p_word in STOPWORDS:
            return True
        else:
            return False

    @staticmethod
    def get_time():
        return math.ceil(time.time()/(60*60*24))

    @staticmethod
    def strip_special_character(p_text):
        m_text = re.sub(r"^\W+", "", p_text)
        return m_text

    @staticmethod
    def split_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]

        m_subhost = p_url[len(m_host_url):]
        if len(m_subhost)==1:
            m_subhost = "na"
        return m_host_url, m_subhost

    @staticmethod
    def join_relative_url(p_url, p_base_url):
        if not p_url.startswith("https://") and not p_url.startswith("http://") and not p_url.startswith("ftp://"):
            m_temp_base_url = p_base_url
            if not m_temp_base_url.endswith("/"):
                m_temp_base_url = m_temp_base_url + "/"
            p_url = requests.compat.urljoin(m_temp_base_url, p_url)
            p_url = p_url.replace(" ", "%20")
            p_url = helper_method.on_clean_url(helper_method.normalize_slashes(p_url))
            return p_url
        else:
            return p_url

    # URL Cleaner
    @staticmethod
    def on_clean_url(p_url):
        if p_url.startswith("http://www.") or p_url.startswith("https://www.") or p_url.startswith("www."):
            p_url = p_url.replace("www.", "", 1)

        while p_url.endswith("/") or p_url.endswith(" "):
            p_url = p_url[:-1]

        return p_url

    # Remove Extra Slashes
    @staticmethod
    def normalize_slashes(p_url):
        p_url = str(p_url)
        segments = p_url.split('/')
        correct_segments = []
        for segment in segments:
            if segment != '':
                correct_segments.append(segment)
        normalized_url = '/'.join(correct_segments)
        normalized_url = normalized_url.replace("http:/","http://")
        normalized_url = normalized_url.replace("https:/","https://")
        normalized_url = normalized_url.replace("ftp:/","ftp://")
        return normalized_url

    @staticmethod
    def is_url_base_64(p_url):
        if str(p_url).startswith("duplicationHandlerService:"):
            return True
        else:
            return False

    @staticmethod
    def is_stop_word(p_word):
        if p_word in STOPWORDS:
            return True
        else:
            return False

    @staticmethod
    def clear_folder(p_path):
        os.chdir(p_path)
        all_files = os.listdir()

        for f in all_files:
            os.remove(f)

    @staticmethod
    def write_content_to_path(p_path, p_content):
        m_url_path = p_path
        file = open(m_url_path, "wb")
        file.write(p_content)
        file.close()

