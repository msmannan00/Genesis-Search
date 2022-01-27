import enum


class USER_INDEX_MODEL_CALLBACK(enum.Enum):
    M_INIT = 1

class USER_INDEX_PARAM:
    M_INDEX_BLOCK = "m_index_block"
    M_INDEX_BLOCK_URL = "m_url"
    M_INDEX_BLOCK_HTML = "m_html"

class USER_INDEX_CALLBACK:
    M_BLOCK_INDEXED_SUCCESS = "service indexed successfully"
    M_BLOCK_INDEXED_FAILED = "service indexed failure"
