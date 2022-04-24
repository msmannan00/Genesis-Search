from orion.controllers.constants.strings import GENERAL_STRINGS


class directory_class_model:
    m_page_number = GENERAL_STRINGS.S_GENERAL_EMPTY
    m_site = GENERAL_STRINGS.S_GENERAL_HTTP
    m_row_model_list = None

    def __init__(self, p_page_number, p_query_row_model_list):
        self.m_page_number = p_page_number
        self.m_row_model_list = p_query_row_model_list
        pass
