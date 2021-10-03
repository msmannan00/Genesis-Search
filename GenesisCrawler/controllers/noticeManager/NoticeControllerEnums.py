import enum


class NoticeModelCommands(enum.Enum):
    M_INIT = 1

class NoticeSessionCommands(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class NoticeParam(str, enum.Enum):
    M_HEADER = "mNoticeParamType"
    M_DATA = "mNoticeParamData"

class NoticeCallback(str, enum.Enum):
    M_TYPE = "mNoticeCallbackType"
    M_DATA = "mNoticeCallbackData"
