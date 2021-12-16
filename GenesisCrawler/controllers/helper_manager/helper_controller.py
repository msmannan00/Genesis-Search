import json
import re
import random, string
from urllib.parse import urlparse
import locale

from gensim.parsing.preprocessing import STOPWORDS


class helper_controller:

    # Private Variables
    __instance = None

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
        if len(p_url)<=0:
            return p_url
        else:
            parsed_uri = urlparse(p_url)
            result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            url = re.compile(r"https?://(www\.)?")
            result = url.sub('', result).strip().strip('/')

            return result

    @staticmethod
    def has_special_character(p_string):
        if bool(re.match('^[a-zA-Z0-9]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def has_spaced_special_character(p_string):
        if bool(re.match('^[a-zA-Z0-9,]*$', p_string)):
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
        if p_word in STOPWORDS:
            return True
        else:
            return False

