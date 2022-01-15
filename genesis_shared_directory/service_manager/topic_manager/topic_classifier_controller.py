# Local Imports
from genesis_shared_directory.request_manager.request_handler import request_handler
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_enums import TOPIC_CLASSFIER_TRAINER, \
    TOPIC_CLASSFIER_MODEL, TOPIC_CLASSFIER_COMMANDS
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_model import topic_classifier_model
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_trainer import topic_classifier_trainer


class topic_classifier_controller(request_handler):

    __instance = None
    __m_classifier_trainer = None
    __m_classifier = None

    # Initializations
    @staticmethod
    def get_instance():
        if topic_classifier_controller.__instance is None:
            topic_classifier_controller()
        return topic_classifier_controller.__instance

    def __init__(self):
        topic_classifier_controller.__instance = self
        self.__m_classifier_trainer = topic_classifier_trainer()
        self.__m_classifier = topic_classifier_model()

    def __predict_classifier(self, p_title,p_description, p_keyword):
        m_cleaned_title = self.__m_classifier_trainer.invoke_trigger(TOPIC_CLASSFIER_TRAINER.S_CLEAN_DATA, [p_title])
        m_cleaned_description = self.__m_classifier_trainer.invoke_trigger(TOPIC_CLASSFIER_TRAINER.S_CLEAN_DATA, [p_description])
        m_cleaned_keyword = self.__m_classifier_trainer.invoke_trigger(TOPIC_CLASSFIER_TRAINER.S_CLEAN_DATA, [p_keyword])

        return self.__m_classifier.invoke_trigger(TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER, [m_cleaned_title, m_cleaned_description, m_cleaned_keyword])

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == TOPIC_CLASSFIER_COMMANDS.S_PREDICT_CLASSIFIER:
            return self.__predict_classifier(p_data[0], p_data[1], p_data[2])
        if p_command == TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER:
            self.__m_classifier.invoke_trigger(TOPIC_CLASSFIER_MODEL.S_LOAD_CLASSIFIER)