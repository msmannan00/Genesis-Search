import enum


class MAINTENANCE_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class MAINTENANCE_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class MAINTENANCE_PARAM:
    M_SECURE_SERVICE = "pSite"

class MAINTENANCE_CALLBACK:
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
