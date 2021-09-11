from GenesisCrawler.constants import strings
from GenesisCrawler.constants.enums import MongoDBCommands
from GenesisCrawler.constants.keys import *
from GenesisCrawler.constants.message import *
from GenesisCrawler.constants.strings import S_DEFAULT_SUBMISSION_RULE_1, S_DEFAULT_SUBMISSION_RULE_2
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.mongoDBManager.mongoDBController import mongoDBController
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapModelCommands


class SitemapModel:

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass

    def validateParameters(self, pData, pContext):
        mValidityStatus = True

        print(pContext[K_SITEMAP_URL])

        mURLModel = mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_FIND_URL, {K_MONGO_SITEMAP_URL: pContext[K_SITEMAP_URL]})

        if pContext[K_SITEMAP_SECRETKEY] == strings.S_GENERAL_EMPTY:
            pContext[K_SITEMAP_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_ERROR
            mValidityStatus = False

        elif len(pContext[K_SITEMAP_SECRETKEY]) < 25:
            pContext[K_SITEMAP_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_MIN_SIZE
            mValidityStatus = False

        elif len(pContext[K_SITEMAP_SECRETKEY]) > 50:
            pContext[K_SITEMAP_SECRETKEY_ERROR] = S_SITEMAP_INVALID_SECRETKEY_MIN_MAX
            mValidityStatus = False

        elif HelperController.hasSpecialCharacter(pContext[K_SITEMAP_SECRETKEY]) is True:
            pContext[K_SITEMAP_SECRETKEY_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            mValidityStatus = False

        if pContext[K_SITEMAP_NAME] == strings.S_GENERAL_EMPTY:
            pContext[K_SITEMAP_NAME_ERROR] = S_SITEMAP_INVALID_NAME_ERROR
            mValidityStatus = False

        elif HelperController.hasSpecialCharacter(pContext[K_SITEMAP_NAME]) is True:
            pContext[K_SITEMAP_NAME_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            mValidityStatus = False

        if pContext[K_SITEMAP_KEYWORD] == strings.S_GENERAL_EMPTY:
            pContext[K_SITEMAP_KEYWORD_ERROR] = S_SITEMAP_INCOMPLETE_KEYWORD_ERROR
            mValidityStatus = False

        elif HelperController.hasSpecialCharacterWithSeperator(pContext[K_SITEMAP_KEYWORD]) is True:
            pContext[K_SITEMAP_KEYWORD_ERROR] = S_GENERAL_INVALID_SECRETKEY_SPECIAL_CHARACTER
            mValidityStatus = False

        if pContext[K_SITEMAP_URL] == strings.S_GENERAL_EMPTY:
            pContext[K_SITEMAP_URL_ERROR] = S_SITEMAP_INCOMPLETE_URL_ERROR
            mValidityStatus = False

        elif pContext[K_SITEMAP_URL].startswith("http") is False:
            pContext[K_SITEMAP_URL_ERROR] = S_SITEMAP_INVALID_URL_ERROR
            mValidityStatus = False

        elif 'onion' not in HelperController.getHost(pContext[K_SITEMAP_URL]):
            pContext[K_SITEMAP_URL_ERROR] = S_SITEMAP_INVALID_URL_SCHEME_ERROR
            mValidityStatus = False

        if pContext[K_SITEMAP_EMAIL] != strings.S_GENERAL_EMPTY and HelperController.isMailValid(pContext[K_SITEMAP_EMAIL]) is False:
            pContext[K_SITEMAP_EMAIL_ERROR] = S_SITEMAP_EMAIL_ERROR
            mValidityStatus = False

        for i in range(1, 6):
            if pContext[(K_SITEMAP_AGREEMENT + str(i))] != strings.S_DEFAULT_RULE:
                mValidityStatus = False
                pContext[K_SITEMAP_RULES_ERROR] = S_SITEMAP_INCOMPLETE_RULES_ERROR

        if mValidityStatus is True:
            if mURLModel is None and pContext[K_SITEMAP_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_2:
                pContext[K_SITEMAP_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_NOT_FOUND
                pContext[K_SITEMAP_URL_ERROR] = S_SITEMAP_URL_NOT_FOUND
                mValidityStatus = False

            if mURLModel is not None and pContext[K_SITEMAP_SECRETKEY] != mURLModel[K_MONGO_SITEMAP_SECRET_KEY]:
                pContext[K_SITEMAP_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_SECRET_KEY_MISMATCH
                pContext[K_SITEMAP_SECRETKEY_ERROR] = S_SITEMAP_URL_SECRET_KEY_MISMATCH
                mValidityStatus = False

            if mURLModel is not None and pContext[K_SITEMAP_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_1:
                pContext[K_SITEMAP_SUBMISSION_RULES_ERROR] = S_SITEMAP_URL_ALREADY_EXISTS
                pContext[K_SITEMAP_URL_ERROR] = S_SITEMAP_URL_ALREADY_EXISTS
                mValidityStatus = False

            mSecretKeyModel = mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_FIND_SECRET_KEY, {K_MONGO_SITEMAP_SECRET_KEY: pContext[K_SITEMAP_SECRETKEY]})
            if mSecretKeyModel is not None and pContext[K_SITEMAP_SUBMISSION_RULES] == S_DEFAULT_SUBMISSION_RULE_1:
                pContext[K_SITEMAP_SUBMISSION_RULES_ERROR] = S_SITEMAP_KEY_ALREADY_EXISTS
                pContext[K_SITEMAP_SECRETKEY_ERROR] = S_SITEMAP_KEY_ALREADY_EXISTS
                mValidityStatus = False

        return pContext, mValidityStatus

    def initAgreement(self, pData, pContext):
        for i in range(1, 6):
            if (K_SITEMAP_PARAM_AGREEMENT + str(i)) in pData.POST:
                pContext[(K_SITEMAP_AGREEMENT + str(i))] = strings.S_DEFAULT_RULE
            else:
                pContext[(K_SITEMAP_AGREEMENT + str(i))] = strings.S_GENERAL_EMPTY
        return pContext

    def uploadWebsite(self, pContext):
        mData = {
            K_MONGO_SITEMAP_URL: pContext[K_SITEMAP_URL],
            K_MONGO_SITEMAP_EMAIL: pContext[K_SITEMAP_EMAIL],
            K_MONGO_SITEMAP_NAME: pContext[K_SITEMAP_NAME],
            K_MONGO_SITEMAP_KEYWORD: pContext[K_SITEMAP_KEYWORD],
            K_MONGO_SITEMAP_SECRET_KEY: pContext[K_SITEMAP_SECRETKEY],
            K_MONGO_SITEMAP_SUBMISSION_RULE: pContext[K_SITEMAP_SUBMISSION_RULES],
        }

        mongoDBController.getInstance().invokeTrigger(MongoDBCommands.M_UPLOAD_URL, mData)

    def initParameters(self, pData):

        mContext = {
            K_SITEMAP_SECRETKEY: strings.S_GENERAL_EMPTY,
            K_SITEMAP_NAME: strings.S_GENERAL_EMPTY,
            K_SITEMAP_URL: strings.S_GENERAL_EMPTY,
            K_SITEMAP_KEYWORD: strings.S_GENERAL_EMPTY,
            K_SITEMAP_EMAIL: strings.S_GENERAL_EMPTY,

            K_SITEMAP_SECRETKEY_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_NAME_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_URL_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_KEYWORD_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_RULES_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_SUBMISSION_RULES: strings.S_DEFAULT_SUBMISSION_RULE_1,
            K_SITEMAP_EMAIL_ERROR: strings.S_GENERAL_EMPTY,
            K_SITEMAP_SUBMISSION_RULES_ERROR: strings.S_GENERAL_EMPTY,
        }

        if K_SITEMAP_PARAM_SECRETKEY in pData.POST:
            mContext[K_SITEMAP_SECRETKEY] = pData.POST[K_SITEMAP_PARAM_SECRETKEY].lower()
        if K_SITEMAP_PARAM_NAME in pData.POST:
            mContext[K_SITEMAP_NAME] = pData.POST[K_SITEMAP_PARAM_NAME]
        if K_SITEMAP_PARAM_URL in pData.POST:
            mContext[K_SITEMAP_URL] = HelperController.getHost(pData.POST[K_SITEMAP_PARAM_URL].lower())
        if K_SITEMAP_PARAM_KEYWORD in pData.POST:
            mContext[K_SITEMAP_KEYWORD] = pData.POST[K_SITEMAP_PARAM_KEYWORD]
        if K_SITEMAP_PARAM_SUBMISSION_RULES in pData.POST:
            mContext[K_SITEMAP_SUBMISSION_RULES] = pData.POST[K_SITEMAP_PARAM_SUBMISSION_RULES]
        if K_SITEMAP_PARAM_EMAIL in pData.POST:
            mContext[K_SITEMAP_EMAIL] = pData.POST[K_SITEMAP_PARAM_EMAIL]

        mContext = self.initAgreement(pData, mContext)

        if len(pData.POST) == 0:
            mContext[K_SITEMAP_SECRETKEY] = HelperController.onCreateSecretKey()
            return mContext, False
        else:
            return mContext, True

    def onInitPage(self, pData):
        mContext, mStatus = self.initParameters(pData)
        if mStatus is False:
            return mContext, False

        mContext, mStatus = self.validateParameters(pData, mContext)
        if mStatus is True and '.onion' in HelperController.getHost(mContext[K_SITEMAP_URL]):
            self.uploadWebsite(mContext)

        return mContext, mStatus

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == SitemapModelCommands.M_INIT:
            return self.onInitPage(pData)
