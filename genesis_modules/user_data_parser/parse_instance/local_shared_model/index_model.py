# Local Imports
import copy
from json import JSONEncoder


class index_model:

    def __init__(self, p_base_url_model, p_title, p_meta_description, p_title_hidden, p_important_content, p_important_content_hidden, p_meta_keywords, p_content, p_content_type, p_sub_url, p_images, p_document, p_video, p_validity_score):
        self.m_base_url_model = p_base_url_model
        self.m_title = p_title
        self.m_meta_description = p_meta_description
        self.m_title_hidden = p_title_hidden
        self.m_important_content = p_important_content
        self.m_important_content_hidden = p_important_content_hidden
        self.m_meta_keywords = p_meta_keywords
        self.m_content = p_content
        self.m_content_type = p_content_type
        self.m_sub_url = p_sub_url
        self.m_images = p_images
        self.m_document = p_document
        self.m_video = p_video
        self.m_validity_score = p_validity_score
        self.m_user_crawled = False

class UrlObjectEncoder(JSONEncoder):
    def default(self, o):
        m_dict = copy.deepcopy(o.__dict__)

        # skip objects for server processing to reduce request load
        if 'm_sub_url' in m_dict:
            del m_dict['m_sub_url']

        return m_dict