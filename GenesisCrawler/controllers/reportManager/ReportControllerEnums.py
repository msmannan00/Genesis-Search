import enum


class ReportModelCommands(enum.Enum):
    M_INIT = 1

class ReportSessionCommands(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class ReportParam(str, enum.Enum):
    M_URL = "pReportParamURL"
    M_EMAIL = "pReportParamEmail"
    M_MESSAGE = "pReportParamMessage"


class ReportCallback(str, enum.Enum):
    M_URL = "mReportCallbackURL"
    M_URL_REDIRECTED = "mReportCallbackRedirectedURL"
    M_EMAIL = "mReportCallbackEmail"
    M_MESSAGE = "mReportCallbackMessage"
    M_URL_ERROR = "mReportURLCallbackError"
    M_EMAIL_ERROR = "mReportEmailCallbackError"

