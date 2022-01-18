import enum


class SITEMAP_MODEL_COMMANDS(enum.Enum):
    M_INIT = 1

class SITEMAP_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class SITEMAP_PARAM(str, enum.Enum):
    M_SECRETKEY = "pSitemapParamSecretKey"
    M_NAME = "pSitemapParamName"
    M_URL = "pSitemapParamURL"
    M_KEYWORD = "pSitemapParamKeyword"
    M_EMAIL = "pSitemapParamEmail"
    M_SUBMISSION_RULES = "pSitemapParamSubmissionRule"
    M_AGREEMENT = "pSitemapParamAgreement_"
    M_SECURE_SERVICE = "pSite"

class SITEMAP_CALLBACK(str, enum.Enum):
    M_SECRETKEY = "mSitemapSecretKeyCallbackValue"
    M_NAME = "mSitemapCallbackNameValue"
    M_URL = "mSitemapCallbackURLValue"
    M_KEYWORD = "mSitemapCallbackKeywordValue"
    M_SUBMISSION_RULES = "mSitemapCallbackSubmissionRule"
    M_EMAIL = "mSitemapCallbackEmailValue"
    M_AGREEMENT = "mSitemapCallbackAgreement_"
    M_SECRETKEY_ERROR = "mSitemapCallbackSecretKeyError"
    M_NAME_ERROR = "mSitemapCallbackNameError"
    M_URL_ERROR = "mSitemapCallbackURLError"
    M_KEYWORD_ERROR = "mSitemapCallbackKeywordError"
    M_RULES_ERROR = "mSitemapCallbackSubmissionError"
    M_EMAIL_ERROR = "mSitemapCallbackEmailError"
    M_SUBMISSION_RULES_ERROR = "mSitemapCallbackSubmissionRulesError"
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
