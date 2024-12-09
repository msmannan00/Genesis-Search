import enum


class LOGIN_MODEL_CALLBACK(enum.Enum):
  M_INIT = 1


class LOGIN_SESSION_COMMANDS(enum.Enum):
  M_INIT = 1
  M_VALIDATE = 2


class LOGIN_PARAM:
  M_ERROR = "pError"


class LOGIN_CALLBACK:
  M_ERROR = "mError"


class LOGIN_CALLBACK_MESSAGES:
  M_LOGIN_FAILED = "Invalid Credentials"
