import enum


class REPORT_MODEL_COMMANDS(enum.Enum):
  M_INIT = 1


class REPORT_SESSION_COMMANDS(enum.Enum):
  M_INIT = 1
  M_VALIDATE = 2


class REPORT_PARAM:
  M_URL = "pReportParamURL"
  M_EMAIL = "pReportParamEmail"
  M_MESSAGE = "pReportParamMessage"
  M_SECURE_SERVICE = "pSite"


class REPORT_CALLBACK:
  M_URL = "mReportCallbackURL"
  M_EMAIL = "mReportCallbackEmail"
  M_MESSAGE = "mReportCallbackMessage"
  M_URL_ERROR = "mReportURLCallbackError"
  M_EMAIL_ERROR = "mReportEmailCallbackError"
  M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
