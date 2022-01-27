import enum


class MANAGE_SEARCH_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class MANAGE_SEARCH_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class MANAGE_SEARCH_PARAM:
    pass

class MANAGE_SEARCH_CALLBACK:
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
