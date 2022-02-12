import re

from modules.user_data_parser.parse_services.constants.strings import GENERIC_STRINGS
from modules.user_data_parser.parse_services.helper_services.spell_check_handler import spell_checker_handler
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.topic_manager.topic_classifier_enums import TOPIC_CLASSFIER_TRAINER


class topic_classifier_trainer(request_handler):

    def __init__(self):
        pass

    def __clean_data(self, p_text):
        # New Line and Tab Remover
        p_text = p_text.replace('\\n', ' ')
        p_text = p_text.replace('\\t', ' ')
        p_text = p_text.replace('\\r', ' ')

        # Lower Case
        p_text = p_text.lower()

        # Remove Special Character
        p_text = re.sub('[^A-Za-z0-9]+', ' ', p_text)

        # Tokenizer
        m_word_list = p_text.split()

        # Word Checking
        m_stemmed_word_list = []
        for m_word in m_word_list:
            m_valid_status = spell_checker_handler.get_instance().validate_word(m_word)
            if m_valid_status is True:
                m_stemmed_word = spell_checker_handler.get_instance().stem_word(m_word)
                m_stemmed_word_list.append(m_stemmed_word)

        return GENERIC_STRINGS.S_SPACE.join(m_stemmed_word_list)

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == TOPIC_CLASSFIER_TRAINER.S_CLEAN_DATA:
            return self.__clean_data(p_data[0])
