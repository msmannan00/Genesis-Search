import enum


class MANAGE_STATUS_MODEL_CALLBACK(enum.Enum):
  M_INIT = 1


class MANAGE_STATUS_SESSION_COMMANDS(enum.Enum):
  M_INIT = 1
  M_VALIDATE = 2


class MANAGE_STATUS_PARAM:
  pass


class MANAGE_STATUS_CALLBACK:
  M_CRONJOB_NOTICE = "mCronjobNotice"
  M_CRONJOB_TIME = "mCronjobTime"
  M_CRAWLER_NOTICE = "mCrawlerNotice"
  M_CRAWLER_TIME = "mCrawlerTime"
