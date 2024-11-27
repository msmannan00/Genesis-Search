import json
import math
import re
import random, string
import secrets
import time
from urllib.parse import urlparse
import locale

import stopwords


class helper_controller:

    # Private Variables
    __instance = None

    @staticmethod
    def id_generator():
        m_id = secrets.token_urlsafe(math.floor(32 / 1.3))
        return m_id

    @staticmethod
    def load_json(p_file_path):
        f = open(p_file_path, )
        return json.load(f)

    @staticmethod
    def is_url_valid(p_url):
      try:
        result = urlparse(p_url)
        return all([result.scheme, result.netloc])
      except ValueError:
        return False

    @staticmethod
    def is_mail_valid(p_email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, p_email):
            return True
        else:
            return False

    @staticmethod
    def get_host(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]

        if len(p_url)==0:
            return ""
        if  m_host_url == "://":
            return p_url

        return m_host_url

    @staticmethod
    def has_special_character(p_string):
        if bool(re.match('^[a-zA-Z0-9]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def has_comma_special_character(p_string):
        if bool(re.match('^[a-zA-Z0-9,]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def has_spaced_special_character(p_string):
        if bool(re.match('^[a-zA-Z0-9\s]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def on_create_secret_key():
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50)).lower()

    @staticmethod
    def on_create_random_search_count(p_doc_size):
        locale.setlocale(locale.LC_ALL, '')
        m_doc_size = 1000 * p_doc_size/10
        m_doc_size = int(m_doc_size*2.36 + ((m_doc_size*2.36 )/2)*3)
        return f'{m_doc_size * 100:n}'

    @staticmethod
    def is_stop_word(p_word):
        if p_word in stopwords.get_stopwords("english"):
            return True
        else:
            return False

    @staticmethod
    def validate_json(jsonData):
        try:
            json.loads(jsonData)
        except ValueError:
            return False
        return True

    @staticmethod
    def get_time():
        return math.ceil(time.time()/(60*60*24))

    @staticmethod
    def get_seconds_since_epoch():
        return int(time.time())

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
