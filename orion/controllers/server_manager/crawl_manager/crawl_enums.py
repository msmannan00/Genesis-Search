import enum


class CRAWL_COMMANDS(enum.Enum):
    M_INIT = 1

class CRAWL_PARAM:
    M_CRAWL_REQUEST_COMMAND = "pRequestCommand"
    M_CRAWL_REQUEST_DATA = "pRequestData"

class CRAWL_CALLBACK:
    M_CRAWL_DATA = "pData"
    M_CRAWL_M_STATUS = "pStatus"

class CRAWL_ERROR_CALLBACK:
    M_INVALID_PARAM = "Invalid Parameters"
    M_CRAWL_M_STATUS = "pStatus"
