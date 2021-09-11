import json
import re
import random, string
from urllib.parse import urlparse


class HelperController:

    # Private Variables
    __instance = None

    @staticmethod
    def loadJSON(pFilePath):
        f = open(pFilePath, )
        return json.load(f)

    @staticmethod
    def isURLValid(pURL):
      try:
        result = urlparse(pURL)
        return all([result.scheme, result.netloc])
      except ValueError:
        return False

    @staticmethod
    def isMailValid(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    @staticmethod
    def getHost(pURL):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, pURL):
            m_parsed_uri = urlparse(pURL)
            m_result = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        else:
            return pURL

    @staticmethod
    def hasSpecialCharacter(pString):
        if bool(re.match('^[a-zA-Z0-9]*$', pString)):
            return False
        else:
            return True

    @staticmethod
    def hasSpecialCharacterWithSeperator(pString):
        if bool(re.match('^[a-zA-Z0-9,]*$', pString)):
            return False
        else:
            return True

    @staticmethod
    def onCreateSecretKey():
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50)).lower()
