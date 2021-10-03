from GenesisCrawler.constants import strings


class QueryRowModel:
    __m_document = strings.S_GENERAL_EMPTY
    __m_category = strings.S_GENERAL_EMPTY

    def __init__(self, p_document, p_category):
        self.__m_document = p_document
        self.__m_category = p_category
        pass

    def get_document(self):
        return self.__m_document

    def get_category(self):
        return self.__m_category

