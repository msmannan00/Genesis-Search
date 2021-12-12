from autocorrect import Speller

from GenesisCrawler.constants import strings
from GenesisCrawler.constants.constant import constants
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelSpellCheckerCommands
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class SpellChecker(RequestHandler):

    # Private Variables
    __instance = None
    __m_speller = None

    # Initializations
    def __init__(self):
        self.__m_speller = Speller(lang=constants.S_GENERAL_DEFAULT_LANGUAGE)
        pass

    def __spell_check_word(self, p_query):
        m_word = self.__m_speller(p_query)
        return m_word

    def __spell_checkl_query(self, p_query):
        m_original_query_filtered = strings.S_GENERAL_EMPTY
        m_misspell = False
        for m_word in p_query:
            m_word_corrected = self.__spell_check_word(m_word)
            if m_word_corrected != m_word:
                m_original_query_filtered += m_word_corrected + strings.S_GENERAL_EMPTY_SPACE
                m_misspell = True
            else:
                m_original_query_filtered += m_word + strings.S_GENERAL_EMPTY_SPACE

        if m_misspell is True:
            return m_original_query_filtered
        else:
            return strings.S_GENERAL_EMPTY

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SearchModelSpellCheckerCommands.M_CHECK_SPELLING:
            return self.__spell_checkl_query(p_data[0])
