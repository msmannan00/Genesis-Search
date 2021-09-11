
class tfModel:
    mDocumentID = None
    mDocumentScore = 0

    def __init__(self, pDocumentID, pDocumentScore):
        self.mDocumentID = pDocumentID
        self.mDocumentScore = pDocumentScore

    def getDocumentScore(self):
        return self.mDocumentScore

    def setDocumentScore(self, pDocumentScore):
        self.mDocumentScore = pDocumentScore
