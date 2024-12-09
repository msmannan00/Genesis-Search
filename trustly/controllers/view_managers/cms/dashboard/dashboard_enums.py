import enum


class DASHBOARD_MODEL_CALLBACK(enum.Enum):
  M_INIT = 1


class DASHBOARD_SESSION_COMMANDS(enum.Enum):
  M_INIT = 1
  M_VALIDATE = 2


class DASHBOARD_PARAM:
  pass


class DASHBOARD_CALLBACK:
  M_SECURE_SERVICE_NOTICE = "mUseSecureServiceNotice"
