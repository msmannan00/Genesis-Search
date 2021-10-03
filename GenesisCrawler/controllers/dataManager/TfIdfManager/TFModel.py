
class TFModel:
    m_document_id = None
    m_document_score = 0

    def __init__(self, p_document_id, p_document_score):
        self.m_document_id = p_document_id
        self.m_document_score = p_document_score

    def get_document_id(self):
        return self.m_document_id

    def get_document_score(self):
        return self.m_document_score

    def set_document_score(self, pDocumentScore):
        self.m_document_score = pDocumentScore
