from GenesisCrawler.constants import strings


class QueryModel:
    __m_search_query = strings.S_GENERAL_EMPTY
    __m_search_type = strings.S_SEARCH_TYPE_PARAM
    __m_page_number = 1
    __m_safe_search = True
    __m_total_documents = 1

    def __init__(self):
        pass

    def get_query(self):
        return self.__m_search_query

    def get_search_type(self):

        return self.__m_search_type

    def get_search_type_mapped(self):
        if self.__m_search_type == "all":
            return "a"
        if self.__m_search_type == "images":
            return "g"
        if self.__m_search_type == "doc":
            return "d"
        if self.__m_search_type == "finance":
            return "b"
        if self.__m_search_type == "news":
            return "n"
        return self.__m_search_type

    def get_page_number(self):
        return self.__m_page_number

    def get_total_documents(self):
        return self.__m_total_documents

    def get_safe_search_status(self):
        return self.__m_safe_search

    def set_query(self, p_search_query):
        self.__m_search_query = p_search_query

    def set_search_type(self, p_search_type):
        if p_search_type != "all" and p_search_type != "images" and p_search_type != "doc" and p_search_type != "finance" and p_search_type != "news":
            self.__m_search_type = strings.S_SEARCH_TYPE_PARAM
        else:
            self.__m_search_type = p_search_type

    def set_page_number(self, p_page_number):
        try:
            self.__m_page_number = int(p_page_number)
        except Exception:
            self.__m_page_number = 1

    def set_total_documents(self, p_total_document):
        try:
            self.__m_total_documents = int(p_total_document)
        except Exception:
            self.__m_total_documents = 1

    def set_safe_search_status(self, p_safe_search):
        self.__m_safe_search = p_safe_search
