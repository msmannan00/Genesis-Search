import re

import nltk
from autocorrect import Speller
from nltk import PorterStemmer

from Genesis.controllers.constants.constant import CONSTANTS
from Genesis.controllers.constants.strings import GENERAL_STRINGS
from Genesis.controllers.helper_manager.helper_controller import helper_controller

nltk.download('punkt')
class spell_checker:

    # Private Variables
    __instance = None
    __m_porter_stemmer = None
    __m_speller = None
    __spell_check = None
    __stemmed_spell_check = None
    __m_score_based_dictionary = {}

    # Initializations
    def __init__(self):
        self.__m_speller = Speller(lang=CONSTANTS.S_GENERAL_DEFAULT_LANGUAGE)
        self.__spell_check = set(open(CONSTANTS.S_DICTIONARY_PATH).read().split())
        self.__stemmed_spell_check = set(open(CONSTANTS.S_STEMMED_DICTIONARY_PATH).read().split())
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

    def __spell_check_word(self, p_query):
        m_word = self.__m_speller(p_query)
        return m_word

    def fetch_invalid_words(self, p_query):
        p_query = p_query.lower()
        m_invalid_words = GENERAL_STRINGS.S_GENERAL_EMPTY
        p_query = p_query.split(" ")

        for m_word in p_query:
            if m_word not in self.__spell_check and m_word not in self.__stemmed_spell_check and helper_controller.has_spaced_special_character(m_word) is False and len(m_word)<10:
                m_invalid_words += m_word + GENERAL_STRINGS.S_GENERAL_EMPTY_SPACE

        return m_invalid_words

    def generate_suggestions(self, p_query, suggestion):
        if len(suggestion) == 0:
            return GENERAL_STRINGS.S_GENERAL_EMPTY, GENERAL_STRINGS.S_GENERAL_EMPTY

        p_query_text = p_query
        for m_suggestion in suggestion:
            if len(m_suggestion['options'])>0:
                p_query = p_query.replace(m_suggestion['text'],"<b style=\"color:#336699\"><u>" +  m_suggestion['options'][0]['text'] + "</u></b>")
                p_query_text = m_suggestion['options'][0]['text']
            else:
                p_query = p_query.replace(m_suggestion['text'],"<b style=\"color:#336699\"><u>" + self.__m_speller.autocorrect_word(m_suggestion['text']) + "</u></b>")
                p_query_text = self.__m_speller.autocorrect_word(m_suggestion['text'])

        return p_query_text, p_query
