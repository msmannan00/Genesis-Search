import re

from GenesisCrawler.controllers.helper_manager.helper_controller import helper_controller
from GenesisCrawler.controllers.search_manager.search_enums import SEARCH_MODEL_TOKENIZATION_COMMANDS
from GenesisCrawler.controllers.shared_model.request_handler import request_handler


class tokenizer(request_handler):

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
            if helper_controller.is_stop_word(p_query[m_range]):
                del p_query[m_range]
            else:
                m_range +=1
            if m_count>100:
                break

        return p_query

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_TOKENIZATION_COMMANDS.M_TOKENIZE:
            return self.onTokenize(p_data[0])
