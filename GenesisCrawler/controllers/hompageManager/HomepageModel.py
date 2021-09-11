from GenesisCrawler.constants.constants import constants
from GenesisCrawler.constants.keys import K_HOME_CALLBACK_REFERENCE
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageModelCommands


class HomepageModel:

    # Private Variables
    __instance = None

    # Initializations
    def __init__(self):
        pass

    def onInitPage(self):
        mContext = {K_HOME_CALLBACK_REFERENCE: HelperController.loadJSON(constants.S_REFERENCE_WEBSITE_URL)}
        return mContext

    # External Request Callbacks
    def invokeTrigger(self, pCommand, pData):
        if pCommand == HomepageModelCommands.M_INIT:
            return self.onInitPage()
