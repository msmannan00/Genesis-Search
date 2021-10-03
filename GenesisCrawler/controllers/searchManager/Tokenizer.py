import re

from GenesisCrawler.constants import strings
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelTokenizerCommands
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class Tokenizer(RequestHandler):

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass

    def onTokenize(self, p_query):
        p_query = re.sub('\W+', ' ', p_query)
        p_query = p_query.lower().split()

        m_range = 0
        for m_count in range(len(p_query)):
            if p_query[m_range] in strings.S_SEARCH_STOP_WORDS:
                del p_query[m_range]
            else:
                m_range +=1
            if m_count>100:
                break

        return p_query

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SearchModelTokenizerCommands.M_TOKENIZE:
            return self.onTokenize(p_data[0])
