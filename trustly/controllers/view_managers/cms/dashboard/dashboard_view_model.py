from trustly.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.dashboard.dashboard_model import dashboard_model


class dashboard_view_model:

    # Private Variables
    __instance = None
    __m_dashboard_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if dashboard_view_model.__instance is None:
            dashboard_view_model()
        return dashboard_view_model.__instance

    def __init__(self):
        if dashboard_view_model.__instance is not None:
            pass
        else:
            dashboard_view_model.__instance = self
            self.__m_dashboard_model = dashboard_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == DASHBOARD_MODEL_CALLBACK.M_INIT:
            m_redirection = self.__m_dashboard_model.invoke_trigger(DASHBOARD_MODEL_CALLBACK.M_INIT, p_data)
            return m_redirection

