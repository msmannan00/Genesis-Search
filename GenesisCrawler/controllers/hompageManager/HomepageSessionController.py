from GenesisCrawler.constants.constant import constants
from GenesisCrawler.controllers.helperManager.helperController import HelperController
from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageCallback, HomepageSessionCommands
from GenesisCrawler.controllers.sharedModel.RequestHandler import RequestHandler


class HomepageSessionController(RequestHandler):

    # Helper Methods
    def __init_parameters(self):
        m_context = {
            HomepageCallback.M_REFERENCE: HelperController.loadJSON(constants.S_REFERENCE_WEBSITE_URL),
            HomepageCallback.M_IS_MOBILE: True
        }
        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HomepageSessionCommands.M_INIT:
            return self.__init_parameters()

