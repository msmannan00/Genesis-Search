import os
from dotenv import load_dotenv

load_dotenv()

class APP_STATUS:
    S_DEVELOPER = True
    S_FERNET_KEY = os.getenv('S_FERNET_KEY')
    S_APP_BLOCK_KEY = os.getenv('S_APP_BLOCK_KEY')
    S_MAINTAINANCE = False


class SERVER_STATUS_TYPE:
    S_SERVER_STATE_DEV_KEY = "S_SERVER_STATE"
    S_SERVER_STATE_DEV = "dev"
    S_SERVER_STATE_PRODUCTION_1 = "production_server_1"
    S_SERVER_STATE_PRODUCTION_2 = "production_server_2"
