import enum


class ERROR_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class ERROR_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class ERROR_PARAM:
    M_SECURE_SERVICE = "pSite"

class ERROR_CALLBACK:
    M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
    M_ERROR_CODE = "mErrorCode"
    M_ERROR_MESSAGE = "mErrorMessage"

class ERROR_MESSAGE_CALLBACK:
    M_ERROR_400 = "mUseSecureServiceNotice"
    M_ERROR_403 = "mUseSecureServiceNotice"
    M_ERROR_500 = "mUseSecureServiceNotice"
    M_ERROR_404 = "mUseSecureServiceNotice"
