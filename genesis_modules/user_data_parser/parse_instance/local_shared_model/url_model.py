# Non Parsed URL Model
import copy
from json import JSONEncoder


class url_model:

    # Initializations
    def __init__(self, p_url, p_depth, p_type):
        self.m_url = p_url
        self.m_redirected_host = p_url
        self.m_depth = p_depth
        self.m_type = p_type

class url_object_encoder(JSONEncoder):
    def default(self, o):
        m_dict = copy.deepcopy(o.__dict__)

        if 'm_sub_url' in m_dict:
            del m_dict['m_sub_url']
            del m_dict['m_response']
            del m_dict['m_thread_id']
            del m_dict['m_validity_score']
            del m_dict['m_base_url_model']

        return m_dict
