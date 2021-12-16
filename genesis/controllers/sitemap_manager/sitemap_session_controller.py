from genesis.constants.enums import MONGO_COMMANDS
from genesis.constants.message import *
from genesis.constants.strings import *
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_CRUD_COMMANDS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.shared_model.request_handler import request_handler
from genesis.controllers.sitemap_manager.sitemap_enums import SITEMAP_SESSION_COMMANDS, SITEMAP_CALLBACK, SITEMAP_PARAM


class sitemap_session_controller(request_handler):

    # Helper Methods
    def initAgreement(self, p_data, p_context):
        for m_count in range(1, 6):
            if (SITEMAP_PARAM.M_AGREEMENT + str(m_count)) in p_data.POST:
                p_context[(SITEMAP_CALLBACK.M_AGREEMENT + str(m_count))] = DEFAULT_STRINGS.S_DEFAULT_RULE
            else:
                p_context[(SITEMAP_CALLBACK.M_AGREEMENT + str(m_count))] = GENERAL_STRINGS.S_GENERAL_EMPTY
        return p_context

    def __init_parameters(self, p_data):
        m_context = {
            SITEMAP_CALLBACK.M_SECRETKEY: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_NAME: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_URL: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_KEYWORD: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_EMAIL: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_SECRETKEY_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_NAME_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_URL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_KEYWORD_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_RULES_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_SUBMISSION_RULES: DEFAULT_STRINGS.S_DEFAULT_SUBMISSION_RULE_1,
            SITEMAP_CALLBACK.M_EMAIL_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR: GENERAL_STRINGS.S_GENERAL_EMPTY,
        }

        if SITEMAP_PARAM.M_SECRETKEY in p_data.POST:
            m_context[SITEMAP_CALLBACK.M_SECRETKEY] = p_data.POST[SITEMAP_PARAM.M_SECRETKEY].lower()
        if SITEMAP_PARAM.M_NAME in p_data.POST:
            m_context[SITEMAP_CALLBACK.M_NAME] = p_data.POST[SITEMAP_PARAM.M_NAME]
        if SITEMAP_PARAM.M_URL in p_data.POST:
            if len(p_data.POST[SITEMAP_PARAM.M_URL])>0:
                if helper_controller.is_url_valid(p_data.POST[SITEMAP_PARAM.M_URL]) is False:
                    m_context[SITEMAP_CALLBACK.M_URL] = p_data.POST[SITEMAP_PARAM.M_URL]
                else:
                    m_context[SITEMAP_CALLBACK.M_URL] = helper_controller.get_host(p_data.POST[SITEMAP_PARAM.M_URL].lower())
        if SITEMAP_PARAM.M_KEYWORD in p_data.POST:
            m_context[SITEMAP_CALLBACK.M_KEYWORD] = p_data.POST[SITEMAP_PARAM.M_KEYWORD]
        if SITEMAP_PARAM.M_SUBMISSION_RULES in p_data.POST:
            m_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES] = p_data.POST[SITEMAP_PARAM.M_SUBMISSION_RULES]
        if SITEMAP_PARAM.M_EMAIL in p_data.POST:
            m_context[SITEMAP_CALLBACK.M_EMAIL] = p_data.POST[SITEMAP_PARAM.M_EMAIL]

        m_context = self.initAgreement(p_data, m_context)
        if len(p_data.POST) == 0:
            m_context[SITEMAP_CALLBACK.M_SECRETKEY] = helper_controller.on_create_secret_key()
            return m_context, False
        else:
            return m_context, True

    def __validate_parameters(self, p_context):
        m_validity_status = True

        m_url_model = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_READ, [MONGO_COMMANDS.M_FIND_URL, {SITEMAP_PARAM.M_URL: p_context[SITEMAP_CALLBACK.M_URL]}])[0]

        if p_context[SITEMAP_CALLBACK.M_SECRETKEY] == GENERAL_STRINGS.S_GENERAL_EMPTY:
            p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_ERROR
            m_validity_status = False

        elif len(p_context[SITEMAP_CALLBACK.M_SECRETKEY]) < 25:
            p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_MIN_SIZE
            m_validity_status = False

        elif len(p_context[SITEMAP_CALLBACK.M_SECRETKEY]) > 50:
            p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_SECRETKEY_MIN_MAX
            m_validity_status = False

        elif helper_controller.has_special_character(p_context[SITEMAP_CALLBACK.M_SECRETKEY]) is True:
            p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SITEMAP_CALLBACK.M_NAME] == GENERAL_STRINGS.S_GENERAL_EMPTY:
            p_context[SITEMAP_CALLBACK.M_NAME_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_NAME_ERROR
            m_validity_status = False

        elif helper_controller.has_special_character(p_context[SITEMAP_CALLBACK.M_NAME]) is True:
            p_context[SITEMAP_CALLBACK.M_NAME_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SITEMAP_CALLBACK.M_KEYWORD] == GENERAL_STRINGS.S_GENERAL_EMPTY:
            p_context[SITEMAP_CALLBACK.M_KEYWORD_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_KEYWORD_ERROR
            m_validity_status = False

        elif helper_controller.has_spaced_special_character(p_context[SITEMAP_CALLBACK.M_KEYWORD]) is True:
            p_context[SITEMAP_CALLBACK.M_KEYWORD_ERROR] = GENERAL_MESSAGES.S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SITEMAP_CALLBACK.M_URL] == GENERAL_STRINGS.S_GENERAL_EMPTY:
            p_context[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_URL_ERROR
            m_validity_status = False

        elif p_context[SITEMAP_CALLBACK.M_URL].startswith(GENERAL_STRINGS.S_GENERAL_HTTP) is False:
            p_context[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_URL_ERROR
            m_validity_status = False

        elif GENERAL_STRINGS.S_GENERAL_ONION_DOMAIN not in helper_controller.get_host(p_context[SITEMAP_CALLBACK.M_URL]):
            p_context[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INVALID_URL_SCHEME_ERROR
            m_validity_status = False

        if p_context[SITEMAP_CALLBACK.M_EMAIL] != GENERAL_STRINGS.S_GENERAL_EMPTY and helper_controller.is_mail_valid(
                p_context[SITEMAP_CALLBACK.M_EMAIL]) is False:
            p_context[SITEMAP_CALLBACK.M_EMAIL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_EMAIL_ERROR
            m_validity_status = False

        for m_count in range(1, 6):
            if p_context[(SITEMAP_CALLBACK.M_AGREEMENT + str(m_count))] != DEFAULT_STRINGS.S_DEFAULT_RULE:
                m_validity_status = False
                p_context[SITEMAP_CALLBACK.M_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_INCOMPLETE_RULES_ERROR

        if m_validity_status is True:
            if m_url_model is None and p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES] == DEFAULT_STRINGS.S_DEFAULT_SUBMISSION_RULE_2:
                p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_NOT_FOUND
                p_context[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_NOT_FOUND
                m_validity_status = False

            if m_url_model is not None and p_context[SITEMAP_CALLBACK.M_SECRETKEY] != m_url_model[SITEMAP_PARAM.M_URL]:
                p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_SECRET_KEY_MISMATCH
                p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_SECRET_KEY_MISMATCH
                m_validity_status = False

            if m_url_model is not None and p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES] == DEFAULT_STRINGS.S_DEFAULT_SUBMISSION_RULE_1:
                p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_ALREADY_EXISTS
                p_context[SITEMAP_CALLBACK.M_URL_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_URL_ALREADY_EXISTS
                m_validity_status = False

            mSecretKeyModel = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_READ, [MONGO_COMMANDS.M_FIND_SECRET_KEY, {SITEMAP_PARAM.M_SECRETKEY: p_context[SITEMAP_CALLBACK.M_SECRETKEY]}])
            if mSecretKeyModel is not None and p_context[
                SITEMAP_CALLBACK.M_SUBMISSION_RULES] == DEFAULT_STRINGS.S_DEFAULT_SUBMISSION_RULE_1:
                p_context[SITEMAP_CALLBACK.M_SUBMISSION_RULES_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_KEY_ALREADY_EXISTS
                p_context[SITEMAP_CALLBACK.M_SECRETKEY_ERROR] = SITEMAP_MESSAGES.S_SITEMAP_KEY_ALREADY_EXISTS
                m_validity_status = False

        return p_context, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SITEMAP_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == SITEMAP_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

