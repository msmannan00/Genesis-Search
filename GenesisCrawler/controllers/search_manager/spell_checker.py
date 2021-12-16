from autocorrect import Speller

from GenesisCrawler.constants.constant import CONSTANTS
from GenesisCrawler.constants.strings import GENERAL_STRINGS
from GenesisCrawler.controllers.search_manager.search_enums import SEARCH_MODEL_SPELL_CHECKER
from GenesisCrawler.controllers.shared_model.request_handler import request_handler


class spell_checker(request_handler):

    # Private Variables
    __instance = None
    __m_speller = None

    # Initializations
    def __init__(self):
        self.__m_speller = Speller(lang=CONSTANTS.S_GENERAL_DEFAULT_LANGUAGE)
        pass

    def __spell_check_word(self, p_query):
        m_word = self.__m_speller(p_query)
        return m_word

    def __spell_checkl_query(self, p_query):
        m_original_query_filtered = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_misspell = False
        for m_word in p_query:
            m_word_corrected = self.__spell_check_word(m_word)
            if m_word_corrected != m_word:
                m_original_query_filtered += m_word_corrected + GENERAL_STRINGS.S_GENERAL_EMPTY_SPACE
                m_misspell = True
            else:
                m_original_query_filtered += m_word + GENERAL_STRINGS.S_GENERAL_EMPTY_SPACE

        if m_misspell is True:
            return m_original_query_filtered
        else:
            return GENERAL_STRINGS.S_GENERAL_EMPTY

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_SPELL_CHECKER.M_CHECK_SPELLING:
            return self.__spell_checkl_query(p_data[0])
