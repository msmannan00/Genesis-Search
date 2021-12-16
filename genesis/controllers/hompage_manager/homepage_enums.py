import enum


class HOMEPAGE_MODEL_COMMANDS(enum.Enum):
    M_INIT = 1

class HOMEPAGE_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class HOMEPAGE_PARAM(enum.Enum):
    pass

class HOMEPAGE_CALLBACK:
    M_REFERENCE = "mHomepageCallbackReference"
    M_IS_MOBILE = "mHomepageCallbackIsMobile"
