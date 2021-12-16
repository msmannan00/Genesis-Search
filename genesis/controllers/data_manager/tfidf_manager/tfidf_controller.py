import math
import operator

from genesis.constants.enums import TFIDF_COMMANDS, MONGO_COMMANDS
from genesis.controllers.data_manager.mongo_manager.mongo_controller import mongo_controller
from genesis.controllers.data_manager.mongo_manager.mongo_enums import MONGODB_CRUD_COMMANDS
from genesis.controllers.data_manager.tfidf_manager.shared_model.tf_model import tf_model
from genesis.controllers.helper_manager.helper_controller import helper_controller


class tfidf_controller:

    __instance = None
    __m_total_document = 0

    __m_tf_model = {}
    __m_idf_model = {}
    __m_info_model = {}

    @staticmethod
    def getInstance():
        if tfidf_controller.__instance is None:
            tfidf_controller()
        return tfidf_controller.__instance

    def __init__(self):
        tfidf_controller.__instance = self
        mDocumentCount = mongo_controller.getInstance().invoke_trigger(MONGODB_CRUD_COMMANDS.S_READ, [MONGO_COMMANDS.M_TOTAL_DOCUMENTS, None])
        self.__m_total_document = mDocumentCount.count()
        self.__m_tfidf_model = {}

    def __get_non_indexed_tokens(self, m_token_list):
        m_token_list_filtered = []
        for m_token in m_token_list:
            if m_token not in self.__m_tfidf_model:
                m_token_list_filtered.append(m_token)

        return m_token_list_filtered

    def __populate_search(self, p_search, p_result):

        # local variables
        m_tf_score = {}
        m_idf_score = {}
        m_tfidf_list_sorted = []

        m_doc_to_url = {}
        m_duplicate_url_penalty = {}
        m_binary_query = []

        m_doc_to_title = {}
        m_duplicate_title_penalty = {}

        m_doc_to_desc = {}
        m_duplicate_desc_penalty = {}

        # if database empty
        if self.__m_total_document == 0:
            return

        # calculate tf score
        for m_document in p_result:
            m_binary_counter=1
            m_tf_score[str(m_document['_id'])] = {}

            for m_binary_word in p_search:
                if len(p_search) > m_binary_counter:
                    m_binary_query.append(m_binary_word + " " + p_search[m_binary_counter])
                    m_binary_counter += 1

                if m_document['_id'] not in m_tf_score:
                    if m_binary_word not in m_document['m_uniary_tfidf_score']:
                        continue
                    m_tf_score[str(m_document['_id'])][m_binary_word] = float(m_document['m_uniary_tfidf_score'][m_binary_word])
                    m_doc_to_url[str(m_document['_id'])] = helper_controller.get_host(m_document['m_url'])
                    m_doc_to_title[str(m_document['_id'])] = m_document['m_title']
                    m_doc_to_desc[str(m_document['_id'])] = m_document['m_description']

                    m_duplicate_url_penalty[m_doc_to_url[str(m_document['_id'])]] = 0
                    m_duplicate_title_penalty[str(m_document['_id'])] = 0
                    m_duplicate_desc_penalty[str(m_document['_id'])] = 0

                    if m_binary_word in m_idf_score:
                        m_idf_score[m_binary_word]+=1
                    else:
                        m_idf_score[m_binary_word]=1

                    # binary tf scores

            for m_binary_word in m_binary_query:
                if m_binary_word not in m_document['m_binary_tfidf_score']:
                    continue

                m_tf_score[str(m_document['_id'])][m_binary_word] = float(m_document['m_binary_tfidf_score'][m_binary_word])

                if m_binary_word in m_idf_score:
                    m_idf_score[m_binary_word]+=1
                else:
                    m_idf_score[m_binary_word]=1

        # calculate idf score
        for m_binary_word in p_search:
            if m_binary_word not in m_idf_score or m_idf_score[m_binary_word] <= 0:
                continue
            try:
                m_idf_score[m_binary_word] = math.log(self.__m_total_document / m_idf_score[m_binary_word])
            except Exception as ex:
                return None

        for m_binary_word in m_binary_query:
            if m_binary_word not in m_idf_score or m_idf_score[m_binary_word] <= 0:
                continue
            try:
                m_idf_score[m_binary_word] = math.log(self.__m_total_document / 2 / m_idf_score[m_binary_word])
            except Exception as ex:
                return None


        # calculate tf-idf score
        m_keys = m_tf_score.keys()
        for m_key in m_keys:
            mTfidfScore = tf_model(m_key, 0)
            # calculate tf-idf score
            for m_token in p_search:
                if m_token not in m_tf_score[m_key]:
                    continue

                mTfidfScore.m_document_score = math.sqrt(math.pow(mTfidfScore.m_document_score, 2) + math.pow(m_idf_score[m_token] * m_tf_score[m_key][m_token], 2))

            for m_binary_token in m_binary_query:
                if m_binary_token in m_tf_score[m_key]:
                    mTfidfScore.m_document_score = math.sqrt(math.pow(mTfidfScore.m_document_score, 2) + math.pow(m_idf_score[m_binary_token] * m_tf_score[m_key][m_binary_token], 2))*2

            # calculate cosine similarity
            if len(m_tfidf_list_sorted) == 0:
                m_tfidf_list_sorted.append(mTfidfScore)
            else:
                mChanged = False

                for index in range(0, len(m_tfidf_list_sorted)):

                    if m_tfidf_list_sorted[index].m_document_score<mTfidfScore.m_document_score:
                        m_tfidf_list_sorted.insert(index, mTfidfScore)
                        mChanged = True
                        break
                if mChanged is False:
                    m_tfidf_list_sorted.append(mTfidfScore)

        m_title_list = []
        m_desc_list = []


        # Repetition Penalty
        for mDocument in m_tfidf_list_sorted:

            if mDocument.m_document_id not in m_doc_to_title:
                break

            if m_doc_to_title[mDocument.m_document_id] not in m_title_list:
                m_title_list.append(m_doc_to_title[mDocument.m_document_id])
                m_duplicate_title_penalty[mDocument.m_document_id] = 0
            else:
                if m_duplicate_title_penalty[mDocument.m_document_id] == 0:
                    m_duplicate_title_penalty[mDocument.m_document_id] = 1
                m_duplicate_title_penalty[mDocument.m_document_id] *= 10


            if m_doc_to_desc[mDocument.m_document_id] not in m_desc_list:
                m_desc_list.append(m_doc_to_desc[mDocument.m_document_id])
                m_duplicate_desc_penalty[mDocument.m_document_id] = 0
            else:
                if m_duplicate_desc_penalty[mDocument.m_document_id] == 0:
                    m_duplicate_desc_penalty[mDocument.m_document_id] = 1
                m_duplicate_desc_penalty[mDocument.m_document_id] *= 2

            m_score_multiplier = m_duplicate_url_penalty[m_doc_to_url[mDocument.m_document_id]]
            if m_score_multiplier==0:
                m_score_multiplier = 1
            else:
                m_score_multiplier *= 2
            m_duplicate_url_penalty[m_doc_to_url[mDocument.m_document_id]] = m_score_multiplier
            mDocument.m_document_score = mDocument.m_document_score / math.sqrt(math.pow(m_score_multiplier, 2) + math.pow(m_duplicate_desc_penalty[mDocument.m_document_id], 2) + math.pow(m_duplicate_title_penalty[mDocument.m_document_id], 2))


        m_tfidf_list_sorted.sort(key=operator.attrgetter("m_document_score"), reverse=True)
        m_tfidf_list_cleaned = sorted(m_tfidf_list_sorted, key=operator.attrgetter("m_document_score"), reverse=True)

        return m_tfidf_list_cleaned

    # External Request Callbacks
    def invoke_trigger(self, p_commands, p_data):
        if p_commands == TFIDF_COMMANDS.M_POPULATE_SEARCH:
            return self.__populate_search(p_data[0], p_data[1])
        if p_commands == TFIDF_COMMANDS.M_GET_NON_INDEXED_TOKENS:
            return self.__get_non_indexed_tokens(p_data[0])
