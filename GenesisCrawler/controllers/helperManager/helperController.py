import json
import re
import random, string
from urllib.parse import urlparse
import locale


class HelperController:

    # Private Variables
    __instance = None

    @staticmethod
    def loadJSON(p_file_path):
        f = open(p_file_path, )
        return json.load(f)

    @staticmethod
    def isURLValid(p_url):
      try:
        result = urlparse(p_url)
        return all([result.scheme, result.netloc])
      except ValueError:
        return False

    @staticmethod
    def isMailValid(p_email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, p_email):
            return True
        else:
            return False

    @staticmethod
    def getHost(p_url):
        if len(p_url)<=0:
            return p_url
        else:
            parsed_uri = urlparse(p_url)
            result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            return result

    @staticmethod
    def hasSpecialCharacter(p_string):
        if bool(re.match('^[a-zA-Z0-9]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def hasSpecialCharacterWithSeperator(p_string):
        if bool(re.match('^[a-zA-Z0-9,]*$', p_string)):
            return False
        else:
            return True

    @staticmethod
    def onCreateSecretKey():
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50)).lower()

    @staticmethod
    def onCreateRandomSearchCount(p_doc_size):
        locale.setlocale(locale.LC_ALL, '')
        m_doc_size = 1000 * p_doc_size/10
        m_doc_size = int(m_doc_size*2.36 + ((m_doc_size*2.36 )/2)*3)
        return f'{m_doc_size * 100:n}'
