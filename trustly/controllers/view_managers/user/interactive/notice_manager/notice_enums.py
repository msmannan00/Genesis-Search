import enum


class NOTICE_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class NOTICE_SESSION_CALLBACK(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class NOTICE_PARAM:
    M_HEADER = "mNoticeParamType"
    M_DATA = "mNoticeParamData"
    M_BROWSER = "browser"
    M_SECURE_SERVICE = "pSite"

class NOTICE_CALLBACK:
    M_TYPE = "mNoticeCallbackType"
    M_DATA = "mNoticeCallbackData"
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
