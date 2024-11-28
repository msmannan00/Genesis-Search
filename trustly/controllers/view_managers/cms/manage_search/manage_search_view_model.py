from trustly.controllers.view_managers.cms.manage_search.manage_search_enums import MANAGE_SEARCH_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.manage_search.manage_search_model import manage_search_model


class manage_search_view_model:

    # Private Variables
    __instance = None
    __m_manage_search_model = None

    # Initializations
    @staticmethod
    def getInstance():
        if manage_search_view_model.__instance is None:
            manage_search_view_model()
        return manage_search_view_model.__instance

    def __init__(self):
        if manage_search_view_model.__instance is not None:
            pass
        else:
            manage_search_view_model.__instance = self
            self.__m_manage_search_model = manage_search_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == MANAGE_SEARCH_MODEL_CALLBACK.M_INIT:
            m_redirection = self.__m_manage_search_model.invoke_trigger(MANAGE_SEARCH_MODEL_CALLBACK.M_INIT, p_data)
            return m_redirection

