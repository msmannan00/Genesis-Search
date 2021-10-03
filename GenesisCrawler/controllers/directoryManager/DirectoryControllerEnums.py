import enum


class DirectoryModelCommands(enum.Enum):
    M_INIT = 1

class DirectorySessionCommands(enum.Enum):
    M_PRE_INIT = 1
    M_INIT = 2
    M_VALIDATE = 3

class DirectoryParam(str, enum.Enum):
    M_PAGE_NUMBER = "mDirectoryParamPageNumber"
    M_PAGE_NUMBER_NEXT = "mDirectoryParamPageNumberNext"
    M_PAGE_NUMBER_PREV = "mDirectoryParamPageNumberPrev"
    M_PAGE_MAX_REACHED = "mDirectoryParamPageNumberMaxReached"

class DirectoryCallback(str, enum.Enum):
    M_PAGE_NUMBER = "mDirectoryCallbackPageNumber"
    M_ONION_LINKS = "mDirectoryCallbackLinks"
    M_MAX_PAGE_REACHED = "mDirectoryCallbackPageNumberMaxReached"

class DirectoryModelCallback(str, enum.Enum):
    M_ID = "mID"
    M_URL = "mURL"
    M_CONTENT_TYPE = "mContentType"
