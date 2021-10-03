import enum


class HomepageModelCommands(enum.Enum):
    M_INIT = 1

class HomepageSessionCommands(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2

class HomepageParam(enum.Enum):
    pass

class HomepageCallback(str,enum.Enum):
    M_REFERENCE = "mHomepageCallbackReference"
    M_IS_MOBILE = "mHomepageCallbackIsMobile"
