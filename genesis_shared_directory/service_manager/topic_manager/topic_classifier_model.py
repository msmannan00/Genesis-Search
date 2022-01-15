import os
import pickle
import pandas as pd

from genesis_modules.user_data_parser.parse_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS
from genesis_modules.user_data_parser.parse_services.constants.constant import shared_constants, classifier_constants
from genesis_modules.user_data_parser.parse_services.constants.strings import GENERIC_STRINGS
from genesis_shared_directory.request_manager.request_handler import request_handler
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_enums import TOPIC_CLASSFIER_MESSAGES, TOPIC_CLASSFIER_MODEL


class topic_classifier_model(request_handler):

    def __init__(self):
        self.__m_vectorizer = None
        self.__m_feature_selector = None
        self.__m_classifier = None
        self.__m_classifier_trained = False
        self.__m_loading = False

    def __classifier_exists(self):
        if self.__m_classifier_trained is not True:
            if os.path.exists(shared_constants.S_PROJECT_PATH + classifier_constants.S_VECTORIZER_PATH) is True and \
               os.path.exists(shared_constants.S_PROJECT_PATH + classifier_constants.S_SELECTKBEST_PATH) is True:
                self.__m_classifier_trained = True
                self.__load_classifier()
                return True
            else:
                return False
        else:
            return True

    def __load_classifier(self):
        if self.__m_loading is False:
            self.__m_loading = True
            self.__m_vectorizer = pickle.load(open(shared_constants.S_PROJECT_PATH + classifier_constants.S_VECTORIZER_PATH, 'rb'))
            self.__m_feature_selector = pickle.load(open(shared_constants.S_PROJECT_PATH + classifier_constants.S_SELECTKBEST_PATH, 'rb'))
            self.__m_classifier = pickle.load(open(shared_constants.S_PROJECT_PATH + classifier_constants.S_CLASSIFIER_PICKLE_PATH, 'rb'))
            self.__m_loading = False

    def __predict_classifier(self, p_title,p_description, p_keyword):
        m_status = self.__classifier_exists()
        if m_status is True:
            try:
                m_title = pd.Series([p_title])
                m_description = pd.Series([p_description])
                m_keyword = pd.Series([p_keyword])

                if m_title is None:
                    m_title = GENERIC_STRINGS.S_EMPTY
                if m_description is None:
                    m_description = GENERIC_STRINGS.S_EMPTY
                if m_keyword is None:
                    m_keyword = []

                m_title_vectorizer_data = self.__m_vectorizer.transform(m_title.values.astype('U'))
                m_description_vectorizer_data = self.__m_vectorizer.transform(m_description.astype('U'))
                m_keyword_vectorizer_data = self.__m_vectorizer.transform(m_keyword.astype('U'))

                m_title_vectorized = pd.DataFrame(m_title_vectorizer_data.toarray(), columns=self.__m_vectorizer.get_feature_names())
                m_description_vectorized = pd.DataFrame(m_description_vectorizer_data.toarray(), columns=self.__m_vectorizer.get_feature_names())
                m_keyword_vectorized = pd.DataFrame(m_keyword_vectorizer_data.toarray(), columns=self.__m_vectorizer.get_feature_names())

                m_dataframe = m_title_vectorized + m_description_vectorized + m_keyword_vectorized

                X = self.__m_feature_selector.transform(m_dataframe)

                m_predictions = list(self.__m_classifier.predict_proba(X)[0])
                max_value = max(m_predictions)
                max_index = m_predictions.index(max_value)

                if max_value > 0.70:
                    m_predictions = self.__m_classifier.classes_[max_index]
                else:
                    m_predictions = CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL

                return m_predictions
            except Exception as ex:
                return CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_UNKNOWN
        else:
            print(TOPIC_CLASSFIER_MESSAGES.S_CLASSIFIER_NOT_TRAINED)

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER:
            return self.__predict_classifier(p_data[0], p_data[1], p_data[2])
        if p_command == TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER:
            self.__load_classifier()
