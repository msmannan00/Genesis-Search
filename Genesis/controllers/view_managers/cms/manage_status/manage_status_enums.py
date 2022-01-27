import enum


class MANAGE_STATUS_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class MANAGE_STATUS_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class MANAGE_STATUS_PARAM:
    pass

class MANAGE_STATUS_CALLBACK:
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
