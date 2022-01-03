import re

from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.search_manager.search_enums import SEARCH_MODEL_TOKENIZATION_COMMANDS
from genesis.controllers.search_manager.spell_checker import spell_checker
from genesis.controllers.shared_model.request_handler import request_handler


class tokenizer(request_handler):

    # Private Variables
    __instance = None
    __m_spell_checker = None

    # Initializations
    def __init__(self):
        self.__m_spell_checker = spell_checker()
        pass

    def onTokenize(self, p_query):
        m_text = p_query

        m_text = m_text.replace('\n', ' ')
        m_text = m_text.replace('\t', ' ')
        m_text = m_text.replace('\r', ' ')
        m_text = m_text.replace(' ', ' ')

        m_text = re.sub(' +', ' ', m_text)

        # Lower Case
        p_text = m_text.lower()

        # Tokenizer
        m_word_tokenized = p_text.split()

        # Word Checking
        m_content = ""
        for m_token in m_word_tokenized:
            if helper_controller.is_stop_word(m_token) is False and m_token.isnumeric() is False:
                m_valid_status = self.__m_spell_checker.validate_word(m_token)
                if m_valid_status is True:
                    m_content += " " + self.__m_spell_checker.stem_word(m_token)
                else:
                    m_content += " " + self.__m_spell_checker.clean_invalid_token(m_token)

        return ' '.join(m_content.split())

    def onSplit(self, p_query):
        m_text = p_query

        m_text = m_text.replace('\n', ' ')
        m_text = m_text.replace('\t', ' ')
        m_text = m_text.replace('\r', ' ')
        m_text = m_text.replace(' ', ' ')

        m_text = re.sub(' +', ' ', m_text)

        # Lower Case
        p_text = m_text.lower()

        # Tokenizer
        m_word_tokenized = p_text.split()

        # Word Checking
        m_content = ""
        for m_token in m_word_tokenized:
            if helper_controller.is_stop_word(m_token) is False and m_token.isnumeric() is False:
                m_valid_status = self.__m_spell_checker.validate_word(m_token)
                if m_valid_status is True:
                    m_content += " " + m_token
                else:
                    m_content += " " + self.__m_spell_checker.clean_invalid_token_non_stemmed(m_token)

        return m_content.split()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_MODEL_TOKENIZATION_COMMANDS.M_TOKENIZE:
            return self.onTokenize(p_data[0])
        if p_command == SEARCH_MODEL_TOKENIZATION_COMMANDS.M_SPLIT_AND_TOKENIZE:
            return self.onSplit(p_data[0])
