import enum


class ErrorMessages(enum.Enum):
    M_SINGLETON_EXCEPTION = 1

class MongoDBCommands(enum.Enum):
     M_REPORT_URL = 1
     M_UPLOAD_URL = 2
     M_FIND_URL = 3
     M_FIND_SECRET_KEY = 4
     M_SEARCH = 5
