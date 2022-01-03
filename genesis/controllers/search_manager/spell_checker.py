import re

import nltk
from autocorrect import Speller
from nltk import PorterStemmer
from genesis.constants.constant import CONSTANTS
from genesis.constants.strings import GENERAL_STRINGS
from genesis.controllers.helper_manager.helper_controller import helper_controller


class spell_checker:

    # Private Variables
    __instance = None
    __m_porter_stemmer = None
    __m_speller = None

    # Initializations
    def __init__(self):
        self.__m_speller = Speller(lang=CONSTANTS.S_GENERAL_DEFAULT_LANGUAGE)
        self.__spell_check = set(open(CONSTANTS.S_DICTIONARY_PATH).read().split())
        self.__m_porter_stemmer = PorterStemmer()
        pass

    def stem_word(self, p_word):
        return self.__m_porter_stemmer.stem(p_word)

    def validate_word(self, p_word):
        if p_word in self.__spell_check:
            return True
        else:
            return False

    def clean_invalid_token(self, p_text):
        m_text = re.sub('[^A-Za-z0-9]+', ' ', p_text)
        m_token_list = nltk.sent_tokenize(m_text)
        m_text_cleaned = ""

        for m_token in m_token_list:
            if helper_controller.is_stop_word(m_token) is False and m_token in self.__spell_check:
                m_text_cleaned += " " + self.stem_word(m_token)

        return m_text_cleaned

    def clean_invalid_token_non_stemmed(self, p_text):
        m_text = re.sub('[^A-Za-z0-9]+', ' ', p_text)
        m_token_list = nltk.sent_tokenize(m_text)
        m_text_cleaned = ""

        for m_token in m_token_list:
            if helper_controller.is_stop_word(m_token) is False and m_token in self.__spell_check:
                m_text_cleaned += " " + m_token

        return m_text_cleaned

    def validate_sentence(self, p_sentence):
        sentences = nltk.sent_tokenize(p_sentence)
        for sentence in sentences:
            p_sentence = sentence.lower()
            m_valid_count = 0
            m_invalid_count = 0
            m_sentence_list = p_sentence.split()
            for word in m_sentence_list:
                if helper_controller.is_stop_word(word) is True or word in self.__spell_check:
                    m_valid_count += 1
                else:
                    m_invalid_count += 1

            if m_valid_count > 0 and m_valid_count / (m_valid_count + m_invalid_count) >= 0.60:
                return " - " + sentence
        return ""

    def spell_check_word(self, p_query):
        m_word = self.__m_speller(p_query)
        return m_word

    def spell_check_query(self, p_query):
        m_original_query_filtered = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_misspell = False
        p_query = p_query.split(" ")
        for m_word in p_query:
            m_word_corrected = self.spell_check_word(m_word)
            if m_word_corrected != m_word:
                m_original_query_filtered += m_word_corrected + GENERAL_STRINGS.S_GENERAL_EMPTY_SPACE
                m_misspell = True
            else:
                m_original_query_filtered += m_word + GENERAL_STRINGS.S_GENERAL_EMPTY_SPACE

        if m_misspell is True:
            return m_original_query_filtered
        else:
            return GENERAL_STRINGS.S_GENERAL_EMPTY