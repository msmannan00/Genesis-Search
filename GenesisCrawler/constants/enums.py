import enum


class MongoDBCommands(enum.Enum):
     M_REPORT_URL = 1
     M_UPLOAD_URL = 2
     M_FIND_URL = 3
     M_FIND_SECRET_KEY = 4
     M_SEARCH = 5
     M_TOTAL_DOCUMENTS = 6
     M_FETCH_DOCUMENTS = 7
     M_ONION_LIST = 8

class TFIDFCommands(enum.Enum):
     M_INIT = 1
     M_POPULATE_SEARCH = 2
     M_GET_NON_INDEXED_TOKENS = 3
