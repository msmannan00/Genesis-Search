# Local Imports
from copy import copy
from genesis_modules.user_data_parser.parse_instance.i_crawl_crawler.html_parse_manager import html_parse_manager
from genesis_modules.user_data_parser.parse_instance.local_shared_model.index_model import index_model

class static_parse_controller:

    m_static_parser = None
    m_html_parser = None

    def __init__(self):
        pass

    def on_parse_html(self, p_html, p_base_url_model):
        m_title, m_meta_description, m_title_hidden,m_important_content, m_important_content_hidden, m_meta_keywords, m_content, m_content_type, m_sub_url, m_images, m_document, m_video, m_validity_score = self.__on_html_parser_invoke(copy(p_base_url_model), p_html)
        return True, index_model(p_base_url_model, m_title, m_meta_description, m_title_hidden, m_important_content, m_important_content_hidden, m_meta_keywords, m_content, m_content_type, m_sub_url, m_images, m_document, m_video, m_validity_score)

    def __on_html_parser_invoke(self, p_base_url, p_html):

        self.m_html_parser = html_parse_manager(p_base_url, p_html)
        self.m_html_parser.feed(p_html)
        return self.m_html_parser.parse_html_files()
