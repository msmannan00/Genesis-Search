from GenesisCrawler.constants import strings


class QueryModel:
    __m_page_number = strings.S_GENERAL_EMPTY
    __m_query_row_model_list = None

    def __init__(self, p_page_number, p_query_row_model_list):
        self.__m_page_number = p_page_number
        self.__m_query_row_model_list = p_query_row_model_list
        pass

    def get_page_number(self):
        return self.__m_page_number

    def get_query_row_model_list(self):
        return self.__m_query_row_model_list

    def set_page_number(self, p_page_number):
        self.__m_page_number = p_page_number

    def set_query_row_model_list(self, p_query_row_model_list):
        self.__m_query_row_model_list = p_query_row_model_list

