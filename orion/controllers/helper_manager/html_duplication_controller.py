# Local Imports
from jaccard_index.jaccard import jaccard_index


class html_duplication_controller:

    __m_duplication_content_handler = []
    __k_score = 6

    # Initializations

    def verify_content_duplication(self, m_content):
        m_max_k_score = 0

        try:
            for doc in self.__m_duplication_content_handler:
                m_score = jaccard_index(doc, m_content, 3)
                if m_score > m_max_k_score:
                    m_max_k_score = m_score

        except Exception as ex:
            print(ex, flush=True)
            pass

        return m_max_k_score

    def on_insert_content(self, m_content):
        self.__m_duplication_content_handler.append(m_content)
