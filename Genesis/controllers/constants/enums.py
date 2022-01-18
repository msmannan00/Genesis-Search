import enum


class MONGO_COMMANDS(enum.Enum):
     M_REPORT_URL = 1
     M_UPLOAD_URL = 2
     M_FIND_URL = 3
     M_FIND_SECRET_KEY = 4
     M_SEARCH_BY_TOKEN = 5
     M_TOTAL_DOCUMENTS = 6
     M_FETCH_DOCUMENT_BY_ID = 7
     M_ONION_LIST = 8

class ELASTIC_COMMANDS(enum.Enum):
     M_INIT = 1
     M_POPULATE_SEARCH = 2
