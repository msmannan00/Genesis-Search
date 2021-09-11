# python manage.py runserver --insecure
# for /f "tokens=5" %a in ('netstat -aon ^| find "8000"') do taskkill /f /pid %a
# Application Server Entry Point

# Libraries
from GenesisCrawler.constants.enums import ErrorMessages

# Server Controller
class ServerController:
    __instance = None
    mSubprocessList = {}
    mSessionData = {}
    mThreadLastID = 0

    # Initializations
    @staticmethod
    def getInstance():
        if ServerController.__instance is None:
            ServerController()
        return ServerController.__instance

    def __init__(self):
        if ServerController.__instance is not None:
            raise Exception(ErrorMessages.M_SINGLETON_EXCEPTION)
        else:
            ServerController.__instance = self

    # External Request Callbacks
    def invokeServer(self, pCommand, pData):
        m_response = None
        return m_response
