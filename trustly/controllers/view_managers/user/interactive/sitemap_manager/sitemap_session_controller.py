from trustly.controllers.constants.enums import MONGO_COMMANDS
from trustly.controllers.constants.message import SITEMAP_MESSAGES, GENERAL_MESSAGES
from trustly.controllers.constants.strings import GENERAL_STRINGS, SITEMAP_STRINGS
from trustly.controllers.helper_manager.helper_controller import helper_controller
from trustly.controllers.view_managers.user.interactive.sitemap_manager.class_model.sitemap_data_model import sitemap_data_model
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_PARAM, SITEMAP_CALLBACK, SITEMAP_SESSION_COMMANDS
from shared_directory.request_manager.request_handler import request_handler
from shared_directory.service_manager.mongo_manager.mongo_controller import mongo_controller
from shared_directory.service_manager.mongo_manager.mongo_enums import MONGODB_CRUD


class sitemap_session_controller(request_handler):

    # Helper Methods
    def __init_agreement(self, p_data, p_sitemap_data_model):
        for m_count in range(1, 6):
            if (SITEMAP_PARAM.M_AGREEMENT + str(m_count)) in p_data.POST:
                p_sitemap_data_model.m_agreement.append(SITEMAP_STRINGS.S_SITEMAP_RULE_DEFAULT_STATE)
            else:
                p_sitemap_data_model.m_agreement.append(GENERAL_STRINGS.S_GENERAL_EMPTY)
        return p_sitemap_data_model

    def __init_parameters(self, p_data):
        m_sitemap_data_model = sitemap_data_model()

        m_sitemap_data_model = self.__init_agreement(p_data, m_sitemap_data_model)
        if SITEMAP_PARAM.M_SECRETKEY in p_data.POST:
            m_sitemap_data_model.m_secret_key = p_data.POST[SITEMAP_PARAM.M_SECRETKEY].lower()
        if SITEMAP_PARAM.M_NAME in p_data.POST:
            m_sitemap_data_model.m_name = p_data.POST[SITEMAP_PARAM.M_NAME]
        if SITEMAP_PARAM.M_URL in p_data.POST:
            m_sitemap_data_model.m_url = helper_controller.get_host(p_data.POST[SITEMAP_PARAM.M_URL].lower())
        if SITEMAP_PARAM.M_KEYWORD in p_data.POST:
            m_sitemap_data_model.m_keyword = p_data.POST[SITEMAP_PARAM.M_KEYWORD]
        if SITEMAP_PARAM.M_SUBMISSION_RULES in p_data.POST:
            m_sitemap_data_model.m_submission_rule = p_data.POST[SITEMAP_PARAM.M_SUBMISSION_RULES]
        if SITEMAP_PARAM.M_EMAIL in p_data.POST:
            m_sitemap_data_model.m_email = p_data.POST[SITEMAP_PARAM.M_EMAIL]
        if SITEMAP_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_sitemap_data_model.p_site = p_data.GET[SITEMAP_PARAM.M_SECURE_SERVICE]

        if len(p_data.POST) == 0:
            m_sitemap_data_model.m_secret_key = helper_controller.on_create_secret_key()

        return m_sitemap_data_model

    def init_callbacks(self, p_sitemap_data_model:sitemap_data_model):
        m_context_response = {}
        m_context_response[SITEMAP_CALLBACK.M_SECRETKEY] = p_sitemap_data_model.m_secret_key
        m_context_response[SITEMAP_CALLBACK.M_NAME] = p_sitemap_data_model.m_name
        m_context_response[SITEMAP_CALLBACK.M_URL] = p_sitemap_data_model.m_url
        m_context_response[SITEMAP_CALLBACK.M_KEYWORD] = p_sitemap_data_model.m_keyword
        m_context_response[SITEMAP_CALLBACK.M_SUBMISSION_RULES] = p_sitemap_data_model.m_submission_rule
        m_context_response[SITEMAP_CALLBACK.M_EMAIL] = p_sitemap_data_model.m_email
        m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_NAME_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_KEYWORD_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_RULES_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_EMAIL_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = GENERAL_STRINGS.S_GENERAL_EMPTY
        m_context_response[SITEMAP_CALLBACK.M_SECURE_SERVICE_NOTICE] = p_sitemap_data_model.p_site


        for m_count in range(0, 5):
            if p_sitemap_data_model.m_agreement[m_count] != SITEMAP_STRINGS.S_SITEMAP_RULE_DEFAULT_STATE:
                m_context_response[SITEMAP_CALLBACK.M_AGREEMENT + str(m_count+1)] = GENERAL_STRINGS.S_GENERAL_EMPTY

        return m_context_response

    def __validate_parameters(self, p_sitemap_data_model:sitemap_data_model):
        if p_sitemap_data_model.m_secret_key is None or p_sitemap_data_model.m_email is None or p_sitemap_data_model.m_url is None or p_sitemap_data_model.m_name is None or p_sitemap_data_model.m_agreement is None or p_sitemap_data_model.m_keyword is None or p_sitemap_data_model.m_submission_rule is None:
            p_sitemap_data_model.set_defaults()
            m_context_response = self.init_callbacks(p_sitemap_data_model)
            return p_sitemap_data_model, m_context_response, False

        m_context_response = self.init_callbacks(p_sitemap_data_model)
        m_validity_status = True

        m_url_model, m_status = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_READ, [MONGO_COMMANDS.M_FIND_URL, [p_sitemap_data_model.m_url], [0,1]])
        if len(list(m_url_model))==0:
            m_url_model = None

        if p_sitemap_data_model.m_secret_key == GENERAL_STRINGS.S_GENERAL_EMPTY:
            m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_ERROR
            m_validity_status = False

        elif len(p_sitemap_data_model.m_secret_key) < 25:
            m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_MIN_SIZE
            m_validity_status = False

        elif len(p_sitemap_data_model.m_secret_key) > 50:
            m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_MIN_MAX
            m_validity_status = False

        elif helper_controller.has_special_character(p_sitemap_data_model.m_secret_key) is True:
            m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_sitemap_data_model.m_name == GENERAL_STRINGS.S_GENERAL_EMPTY:
            m_context_response[SITEMAP_CALLBACK.M_NAME_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_NAME_ERROR
            m_validity_status = False

        elif helper_controller.has_spaced_special_character(p_sitemap_data_model.m_name) is True:
            m_context_response[SITEMAP_CALLBACK.M_NAME_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_sitemap_data_model.m_keyword == GENERAL_STRINGS.S_GENERAL_EMPTY:
            m_context_response[SITEMAP_CALLBACK.M_KEYWORD_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_KEYWORD_ERROR
            m_validity_status = False

        elif helper_controller.has_comma_special_character(p_sitemap_data_model.m_keyword) is True:
            m_context_response[SITEMAP_CALLBACK.M_KEYWORD_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_sitemap_data_model.m_url == GENERAL_STRINGS.S_GENERAL_EMPTY:
            m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_URL_ERROR
            m_validity_status = False

        elif p_sitemap_data_model.m_url.startswith(GENERAL_STRINGS.S_GENERAL_HTTP) is False:
            m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_URL_ERROR
            m_validity_status = False

        elif GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN not in helper_controller.get_host(p_sitemap_data_model.m_url):
            m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_URL_SCHEME_ERROR
            m_validity_status = False

        elif helper_controller.is_url_valid(p_sitemap_data_model.m_url) is False:
            m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_STR_URL_ERROR
            m_validity_status = False

        if p_sitemap_data_model.m_email != GENERAL_STRINGS.S_GENERAL_EMPTY and helper_controller.is_mail_valid(p_sitemap_data_model.m_email) is False:
            m_context_response[SITEMAP_CALLBACK.M_EMAIL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_EMAIL_ERROR
            m_validity_status = False

        for m_count in range(0, 5):
            if p_sitemap_data_model.m_agreement[m_count] != SITEMAP_STRINGS.S_SITEMAP_RULE_DEFAULT_STATE:
                m_validity_status = False
                m_context_response[SITEMAP_CALLBACK.M_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_RULES_ERROR

        if m_validity_status is True:
            if m_url_model is None and p_sitemap_data_model.m_submission_rule == SITEMAP_STRINGS.S_SITEMAP_SUBMISSION_RULE_2:
                m_context_response[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_NOT_FOUND
                m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_NOT_FOUND
                m_validity_status = False

            if m_url_model is not None and p_sitemap_data_model.m_secret_key != m_url_model[SITEMAP_PARAM.M_URL]:
                m_context_response[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_SECRET_KEY_MISMATCH
                m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_SECRET_KEY_MISMATCH
                m_validity_status = False

            if m_url_model is not None and p_sitemap_data_model.m_submission_rule == SITEMAP_STRINGS.S_SITEMAP_SUBMISSION_RULE_1:
                m_context_response[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_ALREADY_EXISTS
                m_context_response[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_ALREADY_EXISTS
                m_validity_status = False

            mSecretKeyModel, m_status = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD.S_READ, [MONGO_COMMANDS.M_FIND_SECRET_KEY, [p_sitemap_data_model.m_secret_key],[None,None]])
            if len(list(mSecretKeyModel)) !=0 and p_sitemap_data_model.m_submission_rule == SITEMAP_STRINGS.S_SITEMAP_SUBMISSION_RULE_1:
                m_context_response[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_KEY_ALREADY_EXISTS
                m_validity_status = False

        return p_sitemap_data_model, m_context_response, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == SITEMAP_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

