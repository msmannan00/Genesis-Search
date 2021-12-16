from genesis.constants.constant import CONSTANTS
from genesis.constants.strings import SEARCH_STRINGS, GENERAL_STRINGS
from genesis.controllers.helper_manager.helper_controller import helper_controller
from genesis.controllers.search_manager.search_enums import SEARCH_SESSION_COMMANDS, SEARCH_PARAM, SEARCH_CALLBACK, SEARCH_DOCUMENT_CALLBACK
from genesis.controllers.search_manager.search_data_model.query_model import query_model
from genesis.controllers.shared_model.request_handler import request_handler


class search_session_controller(request_handler):

    # Helper Methods
    def __init_search_parameters(self, p_data):
        m_query_model = query_model()

        if SEARCH_PARAM.M_QUERY in p_data.GET:
            m_query_model.set_query(p_data.GET[SEARCH_PARAM.M_QUERY])
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

    def __validate_parameters(self, p_context):
        pass

    def __init_parameters(self, p_document_list, p_search_model):
        mRelevanceContextList = []
        mRelatedBusinessList = []
        mRelatedNewsList = []
        mRelatedFilesList = []

        m_links_counter=0
        for m_document in p_document_list:
            m_links_counter+=1
            if p_search_model.m_search_type != SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:
                mRelevanceContext = {
                    SEARCH_CALLBACK.M_TITLE: m_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE],
                    SEARCH_CALLBACK.M_URL: m_document[SEARCH_DOCUMENT_CALLBACK.M_URL],
                    SEARCH_CALLBACK.M_DESCRIPTION: m_document[SEARCH_DOCUMENT_CALLBACK.M_DESCRIPTION][0:230] + GENERAL_STRINGS.S_GENERAL_CONTENT_CONTINUE,
                    SEARCH_CALLBACK.K_SEARCH_TYPE: m_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
                }

                if p_search_model.m_page_number == 1:
                    m_images = m_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]

                    if m_links_counter > CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
                        if m_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE] == 'b':
                            if len(mRelatedBusinessList) < 4:
                                mRelatedBusinessList.append(mRelevanceContext)
                        elif m_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE] == 'n':
                            if len(mRelatedNewsList) < 4:
                                mRelatedNewsList.append(mRelevanceContext)
                        continue
                    elif len(m_images)>0:
                        if len(mRelatedFilesList) < 3:
                            m_url = mRelevanceContext[SEARCH_CALLBACK.M_URL]
                            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_images[0][SEARCH_CALLBACK.M_IMAGE_URL]
                            mRelatedFilesList.append(mRelevanceContext)
                            mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_url

                mRelevanceContextList.append(mRelevanceContext)

            elif p_search_model.get_search_type() == SEARCH_STRINGS.S_SEARCH_CONTENT_TYPE_IMAGE:
                mRelevanceContext = {
                    SEARCH_CALLBACK.M_TITLE: m_document[SEARCH_DOCUMENT_CALLBACK.M_TITLE],
                    SEARCH_CALLBACK.K_SEARCH_TYPE: m_document[SEARCH_DOCUMENT_CALLBACK.M_CONTENT_TYPE],
                }
                m_counter=0
                for m_image_file in m_document[SEARCH_DOCUMENT_CALLBACK.M_IMAGE]:
                    m_counter+=1
                    if m_counter>4:
                        break
                    mRelevanceContext[SEARCH_CALLBACK.M_URL] = m_image_file[SEARCH_CALLBACK.M_IMAGE_URL]
                    if mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a':
                        mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] = m_image_file[SEARCH_CALLBACK.M_IMAGE_TYPE]

                    if p_search_model.get_safe_search_status() == 'False' or p_search_model.get_safe_search_status() == 'True' and mRelevanceContext[SEARCH_CALLBACK.K_SEARCH_TYPE] != 'a':
                        mRelevanceContextList.append(mRelevanceContext)

        if p_search_model.m_page_number<=3:
            min_range = 1
            max_range = 6
        else:
            min_range = p_search_model.m_page_number - 2
            max_range = p_search_model.m_page_number + 3

        m_max_page_reached = False
        if p_search_model.m_total_documents / CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE < max_range:
            max_range = int(p_search_model.m_total_documents / CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE) + 1

            if p_search_model.m_page_number >= max_range-1:
                m_max_page_reached = True

        m_status = True
        if p_search_model.m_page_number > max_range:
            p_search_model.set_page_number(max_range)
            m_max_page_reached = True
            if max_range > 3:
                min_range = max_range-2
            else:
                min_range = 0

        if min_range != max_range:
            m_range = range(min_range,max_range)
        else:
            m_range = None

        mContext = {
            SEARCH_CALLBACK.M_QUERY: p_search_model.m_search_query,
            SEARCH_CALLBACK.M_SAFE_SEARCH: p_search_model.m_safe_search,
            SEARCH_CALLBACK.M_CURRENT_PAGE_NUM: p_search_model.m_page_number,
            SEARCH_CALLBACK.K_SEARCH_TYPE: p_search_model.m_search_type,
            SEARCH_CALLBACK.M_DOCUMENT: mRelevanceContextList,
            SEARCH_CALLBACK.M_PAGE_NUM: m_range,
            SEARCH_CALLBACK.M_MAX_PAGINATION: m_max_page_reached,
            SEARCH_CALLBACK.M_RESULT_COUNT: GENERAL_STRINGS.S_GENERAL_EMPTY,
            SEARCH_CALLBACK.M_RELATED_BUSINESS_SITES: mRelatedBusinessList,
            SEARCH_CALLBACK.M_RELATED_NEWS_SITES: mRelatedNewsList,
            SEARCH_CALLBACK.M_RELATED_FILES: mRelatedFilesList
        }

        if p_search_model.m_total_documents - p_search_model.m_page_number * CONSTANTS.S_SETTINGS_MAX_DOCUMENT_SHOWN_LENGTH>CONSTANTS.S_SETTINGS_SEARCHED_DOCUMENT_SIZE:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = helper_controller.on_create_random_search_count(p_search_model.m_total_documents)
        else:
            mContext[SEARCH_CALLBACK.M_RESULT_COUNT] = p_search_model.m_total_documents


        return mContext, m_status

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == SEARCH_SESSION_COMMANDS.INIT_SEARCH_PARAMETER:
            return self.__init_search_parameters(p_data[0])
        if p_command == SEARCH_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data[0], p_data[1])
        if p_command == SEARCH_SESSION_COMMANDS.M_VALIDATE:
            return self.__validate_parameters(p_data[0])

