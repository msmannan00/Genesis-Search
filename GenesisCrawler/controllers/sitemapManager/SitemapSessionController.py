from GenesisCrawler.constants import strings
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.message import *
from GenesisCrawler.constants.strings import *
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapSessionCommands, SitemapCallback, SitemapParam


class SitemapSessionController(RequestHandler):

    # Helper Methods
    def initAgreement(self, p_data, p_context):
        for m_count in range(1, 6):
            if (SitemapParam.M_AGREEMENT + str(m_count)) in p_data.POST:
                p_context[(SitemapCallback.M_AGREEMENT + str(m_count))] = strings.S_DEFAULT_RULE
            else:
                p_context[(SitemapCallback.M_AGREEMENT + str(m_count))] = strings.S_GENERAL_EMPTY
        return p_context

    def __init_parameters(self, p_data):
        m_context = {
            SitemapCallback.M_SECRETKEY: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_NAME: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_URL: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_KEYWORD: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_EMAIL: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_SECRETKEY_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_NAME_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_URL_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_KEYWORD_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_RULES_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_SUBMISSION_RULES: strings.S_DEFAULT_SUBMISSION_RULE_1,
            SitemapCallback.M_EMAIL_ERROR: strings.S_GENERAL_EMPTY,
            SitemapCallback.M_SUBMISSION_RULES_ERROR: strings.S_GENERAL_EMPTY,
        }

        if SitemapParam.M_SECRETKEY in p_data.POST:
            m_context[SitemapCallback.M_SECRETKEY] = p_data.POST[SitemapParam.M_SECRETKEY].lower()
        if SitemapParam.M_NAME in p_data.POST:
            m_context[SitemapCallback.M_NAME] = p_data.POST[SitemapParam.M_NAME]
        if SitemapParam.M_URL in p_data.POST:
            if len(p_data.POST[SitemapParam.M_URL])>0:
                if HelperController.isURLValid(p_data.POST[SitemapParam.M_URL]) is False:
                    m_context[SitemapCallback.M_URL] = p_data.POST[SitemapParam.M_URL]
                else:
                    m_context[SitemapCallback.M_URL] = HelperController.getHost(p_data.POST[SitemapParam.M_URL].lower())
        if SitemapParam.M_KEYWORD in p_data.POST:
            m_context[SitemapCallback.M_KEYWORD] = p_data.POST[SitemapParam.M_KEYWORD]
        if SitemapParam.M_SUBMISSION_RULES in p_data.POST:
            m_context[SitemapCallback.M_SUBMISSION_RULES] = p_data.POST[SitemapParam.M_SUBMISSION_RULES]
        if SitemapParam.M_EMAIL in p_data.POST:
            m_context[SitemapCallback.M_EMAIL] = p_data.POST[SitemapParam.M_EMAIL]

        m_context = self.initAgreement(p_data, m_context)
        if len(p_data.POST) == 0:
            m_context[SitemapCallback.M_SECRETKEY] = HelperController.onCreateSecretKey()
            return m_context, False
        else:
            return m_context, True

    def __validate_parameters(self, p_context):
        m_validity_status = True

        m_url_model = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_FIND_URL, {
            SitemapParam.M_URL: p_context[SitemapCallback.M_URL]})

        if p_context[SitemapCallback.M_SECRETKEY] == strings.S_GENERAL_EMPTY:
            p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_ERROR
            m_validity_status = False

        elif len(p_context[SitemapCallback.M_SECRETKEY]) < 25:
            p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_MIN_SIZE
            m_validity_status = False

        elif len(p_context[SitemapCallback.M_SECRETKEY]) > 50:
            p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_MIN_MAX
            m_validity_status = False

        elif HelperController.hasSpecialCharacter(p_context[SitemapCallback.M_SECRETKEY]) is True:
            p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SitemapCallback.M_NAME] == strings.S_GENERAL_EMPTY:
            p_context[SitemapCallback.M_NAME_ERROR] = S_SITEMAP_INVALID_NAME_ERROR
            m_validity_status = False

        elif HelperController.hasSpecialCharacter(p_context[SitemapCallback.M_NAME]) is True:
            p_context[SitemapCallback.M_NAME_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SitemapCallback.M_KEYWORD] == strings.S_GENERAL_EMPTY:
            p_context[SitemapCallback.M_KEYWORD_ERROR] = S_SITEMAP_INCOMPLETE_KEYWORD_ERROR
            m_validity_status = False

        elif HelperController.hasSpecialCharacterWithSeperator(p_context[SitemapCallback.M_KEYWORD]) is True:
            p_context[SitemapCallback.M_KEYWORD_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            m_validity_status = False

        if p_context[SitemapCallback.M_URL] == strings.S_GENERAL_EMPTY:
            p_context[SitemapCallback.M_URL_ERROR] = S_SITEMAP_INCOMPLETE_URL_ERROR
            m_validity_status = False

        elif p_context[SitemapCallback.M_URL].startswith(strings.S_GENERAL_HTTP) is False:
            p_context[SitemapCallback.M_URL_ERROR] = S_SITEMAP_INVALID_URL_ERROR
            m_validity_status = False

        elif strings.S_GENERAL_ONION_DOMAIN not in HelperController.getHost(p_context[SitemapCallback.M_URL]):
            p_context[SitemapCallback.M_URL_ERROR] = S_SITEMAP_INVALID_URL_SCHEME_ERROR
            m_validity_status = False

        if p_context[SitemapCallback.M_EMAIL] != strings.S_GENERAL_EMPTY and HelperController.isMailValid(
                p_context[SitemapCallback.M_EMAIL]) is False:
            p_context[SitemapCallback.M_EMAIL_ERROR] = S_SITEMAP_EMAIL_ERROR
            m_validity_status = False

        for m_count in range(1, 6):
            if p_context[(SitemapCallback.M_AGREEMENT + str(m_count))] != strings.S_DEFAULT_RULE:
                m_validity_status = False
                p_context[SitemapCallback.M_RULES_ERROR] = S_SITEMAP_INCOMPLETE_RULES_ERROR

        if m_validity_status is True:
            if m_url_model is None and p_context[SitemapCallback.M_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_2:
                p_context[SitemapCallback.M_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_NOT_FOUND
                p_context[SitemapCallback.M_URL_ERROR] = S_SITEMAP_URL_NOT_FOUND
                m_validity_status = False

            if m_url_model is not None and p_context[SitemapCallback.M_SECRETKEY] != m_url_model[SitemapParam.M_URL]:
                p_context[SitemapCallback.M_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_SECRET_KEY_MISMATCH
                p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_SITEMAP_URL_SECRET_KEY_MISMATCH
                m_validity_status = False

            if m_url_model is not None and p_context[SitemapCallback.M_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_1:
                p_context[SitemapCallback.M_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_ALREADY_EXISTS
                p_context[SitemapCallback.M_URL_ERROR] = S_SITEMAP_URL_ALREADY_EXISTS
                m_validity_status = False

            mSecretKeyModel = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_FIND_SECRET_KEY, {
                SitemapParam.M_SECRETKEY: p_context[SitemapCallback.M_SECRETKEY]})
            if mSecretKeyModel is not None and p_context[
                SitemapCallback.M_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_1:
                p_context[SitemapCallback.M_SUBMISSION_RULES_ERROR] = S_SITEMAP_KEY_ALREADY_EXISTS
                p_context[SitemapCallback.M_SECRETKEY_ERROR] = S_SITEMAP_KEY_ALREADY_EXISTS
                m_validity_status = False

        return p_context, m_validity_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SitemapSessionCommands.M_INIT:
            return self.__init_parameters(p_data[0])
        if p_command == SitemapSessionCommands.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

