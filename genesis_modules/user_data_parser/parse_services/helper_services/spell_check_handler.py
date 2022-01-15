# Local Imports
import re
import nltk

from nltk import PorterStemmer

from genesis_modules.user_data_parser.parse_instance.constants.strings import STRINGS, ERROR_MESSAGES
from genesis_modules.user_data_parser.parse_services.constants.constant import spell_check_constants
from genesis_modules.user_data_parser.parse_services.helper_services.helper_method import helper_method


class spell_checker_handler:
    __instance = None
    __spell_check = None
    __m_porter_stemmer = None

    # Initializations
    @staticmethod
    def get_instance():
        if spell_checker_handler.__instance is None:
            spell_checker_handler()
        return spell_checker_handler.__instance

    def __init__(self):
        if spell_checker_handler.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            spell_checker_handler.__instance = self
            self.__spell_check = set(open(spell_check_constants.S_DICTIONARY_PATH).read().split())
            self.__m_porter_stemmer = PorterStemmer()

    def init_dict(self):
        self.__spell_check = set(open(spell_check_constants.S_DICTIONARY_MINI_PATH).read().split())

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
        m_text_cleaned = STRINGS.S_EMPTY

        for m_token in m_token_list:
            if helper_method.is_stop_word(m_token) is False and m_token in self.__spell_check:
                m_text_cleaned += " " + self.stem_word(m_token)

        return m_text_cleaned

    def validate_sentence(self, p_sentence):
        sentences = nltk.sent_tokenize(p_sentence)
        for sentence in sentences:
            p_sentence = sentence.lower()
            m_valid_count = 0
            m_invalid_count = 0
            m_sentence_list = p_sentence.split()
            for word in m_sentence_list:
                if helper_method.is_stop_word(word) is True or word in self.__spell_check:
                    m_valid_count += 1
                else:
                    m_invalid_count += 1

            if m_valid_count > 0 and m_valid_count / (m_valid_count + m_invalid_count) >= 0.60:
                return " - " + sentence
        return STRINGS.S_EMPTY
