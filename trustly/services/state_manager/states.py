from dotenv import load_dotenv
import os

load_dotenv()
production_mode = os.getenv("PRODUCTION", "0") == "1"
maintainance_mode = os.getenv("MAINTAINANCE", "0") == "1"

class APP_STATUS:
  S_DEVELOPER = not production_mode
  S_MAINTAINANCE = maintainance_mode
