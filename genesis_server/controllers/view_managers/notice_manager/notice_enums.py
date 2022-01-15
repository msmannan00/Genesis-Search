import enum


class NOTICE_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class NOTICE_SESSION_CALLBACK(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class NOTICE_PARAM:
    M_HEADER = "mNoticeParamType"
    M_DATA = "mNoticeParamData"

class NOTICE_CALLBACK:
    M_TYPE = "mNoticeCallbackType"
    M_DATA = "mNoticeCallbackData"
