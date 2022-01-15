import math
import re

from genesis_server.controllers.constants.constant import CONSTANTS
from genesis_server.controllers.constants.strings import SEARCH_STRINGS, GENERAL_STRINGS
from genesis_server.controllers.helper_manager.helper_controller import helper_controller
from genesis_server.controllers.view_managers.search_manager.search_enums import SEARCH_SESSION_COMMANDS, SEARCH_PARAM, SEARCH_CALLBACK, SEARCH_DOCUMENT_CALLBACK
from genesis_server.controllers.view_managers.search_manager.search_data_model.query_model import query_model
from genesis_shared_directory.request_manager.request_handler import request_handler


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
        if SEARCH_PARAM.M_SAFE_SEARCH in p_data.GET:
            if p_data.GET[SEARCH_PARAM.M_SAFE_SEARCH] == "True":
                m_query_model.m_safe_search = "True"
            else:
                m_query_model.m_safe_search = "False"

        return m_query_model

    def __get_page_number(self, p_search_model):
        m_max_page_reached = False
        m_found_pages = math.floor((p_search_model.m_total_documents / CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE) + 1)
        min_range = max(1, p_search_model.m_page_number - 2)

        if p_search_model.m_page_number > 2:
            max_range = p_search_model.m_page_number + min(3, m_found_pages)
        else:
            max_range = math.floor(m_found_pages)

        if m_found_pages < CONSTANTS.S_SETTINGS_MAX_PAGE_SIZE / 2:
            min_range = max(1, int(p_search_model.m_page_number - (CONSTANTS.S_SETTINGS_MAX_PAGE_SIZE - m_found_pages)))
        if p_search_model.m_total_documents < CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
            m_max_page_reached = True
        return min_range, max_range, m_max_page_reached

    def init_callbacks(self, p_search_model, p_min_range, p_max_range, p_max_page_reached, p_relevance_context_list, p_related_business_list, p_related_news_list, p_related_files_list):
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
            SEARCH_CALLBACK.M_RELATED_FILES: p_related_files_list
        }
        return m_context

    def __generate_extra_context(self, p_document, p_relevance_context, p_related_files_list, m_links_counter):
        m_images = p_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]
        p_related_business_list = []
        p_related_news_list = []
        m_continue = False

        if m_links_counter > CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
            if p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE] == 'b':
                if len(p_related_business_list) < 4:
                    p_related_business_list.append(p_relevance_context)
            elif p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE] == 'n':
                if len(p_related_news_list) < 4:
                    p_related_news_list.append(p_relevance_context)
            m_continue = True
        elif len(m_images) > 0:
            if len(p_related_files_list) < 3:
                m_url = p_relevance_context[SEARCH_CALLBACK.M_URL]
                p_relevance_context[SEARCH_CALLBACK.M_URL] = m_images[0]
                p_related_files_list.append(p_relevance_context)
                p_relevance_context[SEARCH_CALLBACK.M_URL] = m_url

        return p_related_business_list, p_related_news_list, p_relevance_context, m_continue

    def __generate_url_context(self, p_document, p_tokenized_query):
        m_title = p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE]
        if len(m_title) < 2:
            m_title = p_document[SEARCH_DOCUMENT_CALLBACK.M_HOST]

        m_description = p_document[SEARCH_DOCUMENT_CALLBACK.M_IMPORTANT_DESCRIPTION][
                        0:230] + GENERAL_STRINGS.S_GENERAL_CONTENT_CONTINUE
        for m_item in p_tokenized_query:
            insensitive_hippo = re.compile(re.escape(m_item), re.IGNORECASE)
            m_description = m_description.replace(m_item, "<b>" + m_item + "</b>")
            insensitive_hippo.sub("<b>" + m_item + "</b>", m_description)

        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: m_title,
            SEARCH_CALLBACK.M_URL: p_document[SEARCH_DOCUMENT_CALLBACK.M_HOST] + p_document[SEARCH_DOCUMENT_CALLBACK.M_SUB_HOST],
            SEARCH_CALLBACK.M_DESCRIPTION: m_description,
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
        }
        return mRelevanceContext

    def __generate_image_content(self, p_document, p_search_model):
        m_relevance_context_list = []
        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE],
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
        }
        m_counter = 0
        for m_image_file in p_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]:
            m_counter += 1
            if m_counter > 4:
                break
            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_image_file[SEARCH_CALLBACK.M_IMAGE_URL]
            if mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a':
                mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] = m_image_file[SEARCH_CALLBACK.M_IMAGE_TYPE]

            if p_search_model.m_safe_search == 'False' or p_search_model.m_safe_search == 'True' and mRelevanceContext[
                SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a':
                m_relevance_context_list.append(mRelevanceContext)
        return m_relevance_context_list

    def __generate_document_content(self, p_document, p_search_model):
        m_relevance_context_list = []
        mRelevanceContext = {
            SEARCH_CALLBACK.M_TITLE: p_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE],
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
        }
        m_counter = 0
        for m_document_file in p_document[SEARCH_DOCUMENT_CALLBACK.M_DOCUMENT]:
            m_counter += 1
            if m_counter > 4:
                break
            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_document_file
            if p_search_model.m_safe_search == 'False' or p_search_model.m_safe_search == 'True' and mRelevanceContext[
                SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a':
                m_relevance_context_list.append(mRelevanceContext)
        return m_relevance_context_list

    def __init_parameters(self, p_document_list, p_search_model, p_tokenized_query):
        m_relevance_context_list = []
        m_related_business_list = []
        m_related_news_list = []
        m_related_files_list = []

        if p_search_model.m_page_number !=1:
            p_document_list=p_document_list[0:CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE]

        m_links_counter=0
        for m_document in p_document_list:

            m_links_counter+=1
            if p_search_model.m_search_type != SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:

                # Generate URL Context
                m_relevance_context = self.__generate_url_context(m_document, p_tokenized_query)

                # Generate Extra Context
                if p_search_model.m_page_number == 1:
                    m_related_business_list_re, m_related_news_list_re, m_relevance_context, m_continue = self.__generate_extra_context(m_document, m_relevance_context, m_related_files_list, m_links_counter)
                    m_related_business_list_re.__add__(m_related_business_list)
                    m_related_news_list.__add__(m_related_news_list_re)
                    if m_continue is True:
                        continue

                m_relevance_context_list.append(m_relevance_context)

            # Generate Image Context
            elif p_search_model.m_search_type == SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:
                m_relevance_context_list.__add__(self.__generate_image_content(m_document, p_search_model))

            # Generate Document Context
            elif p_search_model.m_search_type == SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_DOCUMENT:
                m_relevance_context_list.__add__(self.__generate_document_content(m_document, p_search_model))

        # Pagination Calculator
        min_range, max_range, m_max_page_reached = self.__get_page_number(p_search_model)

        # Init Callback
        mContext = self.init_callbacks(p_search_model, min_range, max_range, m_max_page_reached, m_relevance_context_list, m_related_business_list, m_related_news_list, m_related_files_list)

        if p_search_model.m_total_documents >= 80:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = helper_controller.on_create_random_search_count(p_search_model.m_total_documents)
        else:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = p_search_model.m_total_documents

        return mContext, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER:
            return self.__init_search_parameters(p_data[0])
        if p_command == SEARCH_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0], p_data[1], p_data[2])

