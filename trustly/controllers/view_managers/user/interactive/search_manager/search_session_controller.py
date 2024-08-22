from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.strings import GENERAL_STRINGS, SEARCH_STRINGS
from trustly.controllers.helper_manager.helper_controller import helper_controller
from trustly.controllers.view_managers.user.interactive.search_manager.search_data_model.query_model import query_model
from trustly.controllers.view_managers.user.interactive.search_manager.search_enums import SEARCH_PARAM, SEARCH_CALLBACK, SEARCH_DOCUMENT_CALLBACK, SEARCH_SESSION_COMMANDS
from app_manager.request_manager.request_handler import request_handler


class search_session_controller(request_handler):

    # Helper Methods
    def __init_search_parameters(self, p_data):
        m_query_model = query_model()

        if SEARCH_PARAM.M_QUERY in p_data.GET:
            m_query_model.set_query(p_data.GET[SEARCH_PARAM.M_QUERY][0:150])
        if SEARCH_PARAM.M_TYPE in p_data.GET:
            m_query_model.m_search_type=p_data.GET[SEARCH_PARAM.M_TYPE]
        if SEARCH_PARAM.M_PAGE in p_data.GET:
            m_query_model.set_page_number(p_data.GET[SEARCH_PARAM.M_PAGE])
        if SEARCH_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_query_model.m_site = p_data.GET[SEARCH_PARAM.M_SECURE_SERVICE]
        if SEARCH_PARAM.M_SAFE_SEARCH in p_data.GET:
            if p_data.GET[SEARCH_PARAM.M_SAFE_SEARCH] == "True":
                m_query_model.m_safe_search = "True"
            else:
                m_query_model.m_safe_search = "False"

        return m_query_model

    def __get_page_number(self, p_search_model):

        min_range = 1
        if p_search_model.m_page_number==1:
            if CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE > p_search_model.m_total_documents:
                m_max_page_reached = True
                max_range = p_search_model.m_page_number
            else:
                m_max_page_reached = False
                max_range = p_search_model.m_page_number + 2
        else:
            if p_search_model.m_total_documents>0:
                m_max_page_reached = False
                max_range = p_search_model.m_page_number + 2
            else:
                m_max_page_reached = False
                max_range = p_search_model.m_page_number+1

        if p_search_model.m_total_documents == 0:
            m_max_page_reached = True

        if p_search_model.m_page_number>2:
            min_range = p_search_model.m_page_number - 1

        return min_range, max_range, m_max_page_reached

    def init_callbacks(self, p_search_model:query_model, p_min_range, p_max_range, p_max_page_reached, p_relevance_context_list, p_related_business_list, p_related_news_list, p_related_files_list):
        m_context = {
            SEARCH_CALLBACK.M_QUERY: p_search_model.m_search_query,
            SEARCH_CALLBACK.M_SAFE_SEARCH: p_search_model.m_safe_search,
            SEARCH_CALLBACK.M_CURRENT_PAGE_NUM: p_search_model.m_page_number,
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_search_model.m_search_type,
            SEARCH_CALLBACK.M_DOCUMENT: p_relevance_context_list,
            SEARCH_CALLBACK.M_PAGE_NUM: range(p_min_range, p_max_range),
            SEARCH_CALLBACK.M_MAX_PAGINATION: p_max_page_reached,
            SEARCH_CALLBACK.M_RESULT_COUNT: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SEARCH_CALLBACK.M_RELATED_BUSINESS_SITES: p_related_business_list,
            SEARCH_CALLBACK.M_RELATED_NEWS_SITES: p_related_news_list,
            SEARCH_CALLBACK.M_RELATED_FILES: p_related_files_list,
            SEARCH_CALLBACK.M_SECURE_SERVICE_NOTICE: p_search_model.m_site,
            SEARCH_CALLBACK.M_HATE_QUERY: p_search_model.m_hate_query
        }

        return m_context

    def __generate_extra_context(self, p_document, p_relevance_context, p_related_files_list, m_links_counter):
        m_images = p_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]
        p_related_business_list = []
        p_related_news_list = []
        m_continue = False


        if m_links_counter > CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
            pass
        elif len(m_images) > 0:
            if len(p_related_files_list) < 3:
                m_url = p_relevance_context[SEARCH_CALLBACK.M_URL]
                p_relevance_context[SEARCH_CALLBACK.M_URL] = m_images[0]
                p_related_files_list.append(p_relevance_context)
                p_relevance_context[SEARCH_CALLBACK.M_URL] = m_url

        return p_related_business_list, p_related_news_list, p_relevance_context, m_continue

    def ireplace(self, old, repl, text):
        m_tokenize_description = text.split(" ")
        m_description = GENERAL_STRINGS.S_GENERAL_EMPTY

        for m_token in m_tokenize_description:
            if old == m_token:
                m_description += repl + " "
            elif old in m_token:
                if ">" in m_description or "<" in m_description:
                    m_description += repl + " "
                else:
                    m_description += "<span style='color:#4d4d4d;font-weight:600'>" + m_token + "</span>" + " "
            else:
                m_description += m_token + " "
        return m_description

    def __generate_url_context(self, p_document, p_tokenized_query, p_search_model):
        m_title = p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE]
        if len(m_title) < 2:
            m_title = p_document[SEARCH_DOCUMENT_CALLBACK.M_HOST]

        m_description = p_document[SEARCH_DOCUMENT_CALLBACK.M_IMPORTANT_DESCRIPTION] + GENERAL_STRINGS.S_GENERAL_CONTENT_CONTINUE
        m_index = 10000

        m_query = ' '.join(p_tokenized_query)
        if m_query in m_description and m_query.count(" ")>2:
            m_index = m_description.index(m_query)
            if m_description[m_index-20:m_index].__contains__(" "):
                m_space_index = m_description.index(" ", m_index-20,m_index)
            else:
                m_space_index = m_index
            m_description = m_description[m_space_index:m_space_index+250]
            m_description_original = m_description[m_space_index:m_space_index+250]
            m_description = m_description.replace(m_query, "<span style=\"color:#4d4d4d;font-weight:600\">" + m_query + "</span>")
        else:
            for m_item in p_tokenized_query:
                if m_item in m_description.lower():
                    m_item_index = m_description.lower().index(m_item)
                    if m_item_index < m_index:
                        m_index = m_item_index

            m_description = m_description[0:250]
            m_description_original = m_description
            for m_item in p_tokenized_query:
                if helper_controller.is_stop_word(m_item.lower()) is True:
                    continue
                m_description = self.ireplace(m_item, "<span style=\"color:#4d4d4d;font-weight:600\">" + m_item + "</span>", m_description)

        m_description = m_description.lstrip(" -")
        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: self.__normalize_text(m_title),
            SEARCH_CALLBACK.M_URL: p_document[SEARCH_DOCUMENT_CALLBACK.M_HOST] + p_document[SEARCH_DOCUMENT_CALLBACK.M_SUB_HOST],
            SEARCH_CALLBACK.M_DESCRIPTION: m_description,
        }
        mRelevanceContextOriginal = {
            SEARCH_CALLBACK.M_TITLE: self.__normalize_text(m_title),
            SEARCH_CALLBACK.M_URL: p_document[SEARCH_DOCUMENT_CALLBACK.M_HOST] + p_document[SEARCH_DOCUMENT_CALLBACK.M_SUB_HOST],
            SEARCH_CALLBACK.M_DESCRIPTION: m_description_original,
        }

        if p_search_model.m_safe_search == 'False' or (str(p_search_model.m_safe_search) == 'True' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'adult'):
            return mRelevanceContext, mRelevanceContextOriginal
        else:
            return None, None

    def __generate_image_content(self, p_document, p_search_model, m_direct_url_list):

        m_relevance_context_list = []

        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: self.__normalize_text(p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE]),
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
        }
        m_counter = 0
        for m_image_file in p_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]:
            if m_image_file[SEARCH_CALLBACK.M_IMAGE_URL] not in m_direct_url_list:
                m_direct_url_list.append(m_image_file[SEARCH_CALLBACK.M_IMAGE_URL])
            else:
                continue

            if m_counter > 4:
                break

            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_image_file[SEARCH_CALLBACK.M_IMAGE_URL]
            if mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'adult' and mRelevanceContext not in m_relevance_context_list:
                mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] = m_image_file[SEARCH_CALLBACK.M_IMAGE_TYPE]

            if p_search_model.m_safe_search == 'False' or (str(p_search_model.m_safe_search) == 'True' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'adult'):
                m_counter += 1
                m_relevance_context_list.append({"mSearchCallbackRelevantDocumentURL": m_image_file[SEARCH_CALLBACK.M_IMAGE_URL]})

        return m_relevance_context_list, m_direct_url_list

    def __generate_document_content(self, p_document, p_search_model, m_direct_url_list):
        m_relevance_context_list = []
        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: self.__normalize_text(p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE]),
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
        }
        m_counter = 0
        for m_document_file in p_document[SEARCH_DOCUMENT_CALLBACK.M_DOCUMENT]:
            if m_document_file not in m_direct_url_list:
                m_direct_url_list.append(m_document_file)
            else:
                continue

            if m_counter > 4:
                break
            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_document_file

            if p_search_model.m_safe_search == 'False' or (str(p_search_model.m_safe_search) == 'True' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'adult'):
                m_counter += 1
                m_relevance_context_list.append({"mSearchCallbackRelevantDocumentURL": m_document_file})
        return m_relevance_context_list

    def __normalize_text(self, p_text):
        return p_text.encode("ascii", "ignore").decode()

    def __init_parameters(self, p_document_list, p_search_model):
        m_relevance_context_list = []
        m_related_business_list = []
        m_related_news_list = []
        m_related_files_list = []
        m_direct_url_list = []

        p_tokenized_query = p_search_model.m_search_query.lower().split(" ")

        if p_search_model.m_page_number !=1:
            p_document_list=p_document_list[0:CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE]

        m_links_counter=0
        for m_document in p_document_list:

            m_links_counter+=1
            if p_search_model.m_search_type != SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:

                # Generate URL Context
                m_relevance_context, m_relevance_context_original = self.__generate_url_context(m_document, p_tokenized_query, p_search_model)

                # Generate Extra Context
                if p_search_model.m_page_number == 1 and m_relevance_context_original is not None and m_relevance_context_original is not None:
                    m_related_business_list_re, m_related_news_list_re, m_relevance_context_original, m_continue = self.__generate_extra_context(m_document, m_relevance_context_original, m_related_files_list, m_links_counter)
                    if len(m_related_business_list)<5 and len(m_related_business_list_re)>0:
                        m_related_business_list.extend(m_related_business_list_re)
                    if len(m_related_news_list)<5 and len(m_related_news_list_re)>0:
                        m_related_news_list.extend(m_related_news_list_re)

                    if m_continue is True:
                        continue

                if m_relevance_context is not None:
                    m_relevance_context_list.append(m_relevance_context)

            # Generate Image Context
            elif p_search_model.m_search_type == SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:
                m_list, m_direct_url_list = self.__generate_image_content(m_document, p_search_model, m_direct_url_list)
                if len(m_list) > 0:
                    m_relevance_context_list.extend(m_list)

            # Generate Document Context
            elif p_search_model.m_search_type == SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_DOCUMENT:
                m_list, m_direct_url_list = self.__generate_document_content(m_document, p_search_model, m_direct_url_list)
                m_relevance_context_list.extend(m_list)

        # Pagination Calculator
        min_range, max_range, m_max_page_reached = self.__get_page_number(p_search_model)

        # Init Callback
        mContext = self.init_callbacks(p_search_model, min_range, max_range, m_max_page_reached, m_relevance_context_list, m_related_business_list, m_related_news_list, m_related_files_list)

        if p_search_model.m_total_documents >= CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = helper_controller.on_create_random_search_count(p_search_model.m_total_documents)
        else:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = p_search_model.m_total_documents

        return mContext, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER:
            return self.__init_search_parameters(p_data[0])
        if p_command == SEARCH_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0], p_data[1])

