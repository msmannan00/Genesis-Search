import math
import operator
from GenesisCrawler.constants.enums import TFIDFCommands, MongoDBCommands
from GenesisCrawler.controllers.dataManager.TfIdfManager.TFModel import TFModel
from GenesisCrawler.controllers.dataManager.mongoDBManager.MongoDBController import MongoDBController
from GenesisCrawler.controllers.helperManager.helperController import HelperController


class TfIdfController:

    __instance = None
    m_total_document = 0
    m_tfidf_model = {}

    @staticmethod
    def getInstance():
        if TfIdfController.__instance is None:
            TfIdfController()
        return TfIdfController.__instance

    def __init__(self):
        TfIdfController.__instance = self
        mDocumentCount = MongoDBController.getInstance().invoke_trigger(MongoDBCommands.M_TOTAL_DOCUMENTS, None)
        self.m_total_document = mDocumentCount

    def __get_non_indexed_tokens(self, m_token_list):
        m_token_list_filtered = []
        for m_token in m_token_list:
            if m_token not in self.m_tfidf_model:
                m_token_list_filtered.append(m_token)

        return m_token_list_filtered

    def __populate_search(self, p_search, p_result):

        # local variables
        m_tf_score = {}
        m_idf_score = {}
        m_tfidf_list_sorted = []

        m_doc_to_url = {}
        m_duplicate_url_penalty = {}

        m_doc_to_title = {}
        m_duplicate_title_penalty = {}

        m_doc_to_desc = {}
        m_duplicate_desc_penalty = {}

        # if database empty
        if self.m_total_document == 0:
            return

        # calculate tf score
        for m_document in p_result:
            m_binary_counter=1
            m_tf_score[str(m_document['_id'])] = {}

            for m_word in p_search:
                if m_document['_id'] not in m_tf_score:
                    if m_word not in m_document['m_score']:
                        m_binary_counter += 1
                        continue
                    m_tf_score[str(m_document['_id'])][m_word] = float(m_document['m_score'][m_word])
                    m_doc_to_url[str(m_document['_id'])] = HelperController.getHost(m_document['m_url'])
                    m_doc_to_title[str(m_document['_id'])] = m_document['m_title']
                    m_doc_to_desc[str(m_document['_id'])] = m_document['m_description']

                    m_duplicate_url_penalty[m_doc_to_url[str(m_document['_id'])]] = 0
                    m_duplicate_title_penalty[str(m_document['_id'])] = 0
                    m_duplicate_desc_penalty[str(m_document['_id'])] = 0

                    if m_word in m_idf_score:
                        m_idf_score[m_word]+=1
                    else:
                        m_idf_score[m_word]=1

                    # binary tf scores
                    if len(p_search)<=m_binary_counter:
                        m_binary_counter += 1
                        continue

                    m_binary_word = m_word + " " + p_search[m_binary_counter]
                    if m_binary_word not in m_document['m_binary_score']:
                        continue

                    m_tf_score[str(m_document['_id'])][m_binary_word] = float(m_document['m_binary_score'][m_binary_word])

                    m_binary_counter+=1
                    if m_binary_word in m_idf_score:
                        m_idf_score[m_binary_word]+=1
                    else:
                        m_idf_score[m_binary_word]=1

        # calculate idf score
        m_binary_counter = 1
        for m_word in p_search:
            if m_word not in m_idf_score or m_idf_score[m_word] <= 0:
                continue
            try:
                m_idf_score[m_word] = math.log(self.m_total_document / m_idf_score[m_word])
            except Exception:
                return None

            # binary tf scores
            if len(p_search) <= m_binary_counter:
                continue

            m_binary_word = m_word + " " + p_search[m_binary_counter]
            if m_binary_word in m_idf_score:
                m_binary_counter+=1
                m_idf_score[m_binary_word] = math.log(self.m_total_document/2 / m_idf_score[m_binary_word])

        # calculate tf-idf score
        m_keys = m_tf_score.keys()
        for m_key in m_keys:
            mTfidfScore = TFModel(m_key, 0)
            # calculate tf-idf score
            m_binary_counter = 0
            for m_token in p_search:
                if m_token not in m_tf_score[m_key]:
                    continue

                mTfidfScore.set_document_score(math.sqrt(math.pow(mTfidfScore.m_document_score, 2) + math.pow(m_idf_score[m_token] * m_tf_score[m_key][m_token], 2)))

                m_binary_counter+=1
                if len(p_search) <= m_binary_counter:
                    continue

                m_binary_word = m_token + " " + p_search[m_binary_counter]
                if m_binary_word not in m_tf_score[m_key]:
                    continue

                mTfidfScore.set_document_score(math.sqrt(math.pow(mTfidfScore.m_document_score, 2) + math.pow(m_idf_score[m_binary_word] * m_tf_score[m_key][m_binary_word], 2)))

            # calculate cosine similarity
            if len(m_tfidf_list_sorted) == 0:
                m_tfidf_list_sorted.append(mTfidfScore)
            else:
                mChanged = False

                for index in range(0, len(m_tfidf_list_sorted)):

                    if m_tfidf_list_sorted[index].get_document_score()<mTfidfScore.get_document_score():
                        m_tfidf_list_sorted.insert(index, mTfidfScore)
                        mChanged = True

                        break
                if mChanged is False:
                    m_tfidf_list_sorted.append(mTfidfScore)

        m_title_list = []
        m_desc_list = []


        # Repetition Penalty
        for mDocument in m_tfidf_list_sorted:

            if mDocument.get_document_id() not in m_doc_to_title:
                break

            if m_doc_to_title[mDocument.get_document_id()] not in m_title_list:
                m_title_list.append(m_doc_to_title[mDocument.get_document_id()])
                m_duplicate_title_penalty[mDocument.get_document_id()] = 0
            else:
                if m_duplicate_title_penalty[mDocument.get_document_id()] == 0:
                    m_duplicate_title_penalty[mDocument.get_document_id()] = 1
                m_duplicate_title_penalty[mDocument.get_document_id()] *= 10


            if m_doc_to_desc[mDocument.get_document_id()] not in m_desc_list:
                m_desc_list.append(m_doc_to_desc[mDocument.get_document_id()])
                m_duplicate_desc_penalty[mDocument.get_document_id()] = 0
            else:
                if m_duplicate_desc_penalty[mDocument.get_document_id()] == 0:
                    m_duplicate_desc_penalty[mDocument.get_document_id()] = 1
                m_duplicate_desc_penalty[mDocument.get_document_id()] *= 2

            m_score_multiplier = m_duplicate_url_penalty[m_doc_to_url[mDocument.get_document_id()]]
            if m_score_multiplier==0:
                m_score_multiplier = 1
            else:
                m_score_multiplier *= 2
            m_duplicate_url_penalty[m_doc_to_url[mDocument.m_document_id]] = m_score_multiplier
            mDocument.set_document_score(mDocument.get_document_score() / math.sqrt(math.pow(m_score_multiplier, 2) + math.pow(m_duplicate_desc_penalty[mDocument.get_document_id()], 2) + math.pow(m_duplicate_title_penalty[mDocument.get_document_id()], 2)))


        m_tfidf_list_sorted.sort(key=operator.attrgetter("m_document_score"), reverse=True)
        m_tfidf_list_cleaned = sorted(m_tfidf_list_sorted, key=operator.attrgetter("m_document_score"), reverse=True)


        return m_tfidf_list_cleaned

    # External Request Callbacks
    def invoke_trigger(self, p_commands, p_data):
        if p_commands == TFIDFCommands.M_POPULATE_SEARCH:
            return self.__populate_search(p_data[0], p_data[1])
        if p_commands == TFIDFCommands.M_GET_NON_INDEXED_TOKENS:
            return self.__get_non_indexed_tokens(p_data[0])
