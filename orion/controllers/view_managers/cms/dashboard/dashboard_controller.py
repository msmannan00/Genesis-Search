from orion.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_MODEL_CALLBACK
from orion.controllers.view_managers.cms.dashboard.dashboard_model import dashboard_model


class dashboard_controller:

    # Private Variables
    __instance = None
    __m_dashboard_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if dashboard_controller.__instance is None:
            dashboard_controller()
        return dashboard_controller.__instance

    def __init__(self):
        if dashboard_controller.__instance is not None:
            pass
        else:
            dashboard_controller.__instance = self
            self.__m_dashboard_model = dashboard_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DASHBOARD_MODEL_CALLBACK.M_INIT:
            m_redirection = self.__m_dashboard_model.invoke_trigger(DASHBOARD_MODEL_CALLBACK.M_INIT, p_data)
            return m_redirection

