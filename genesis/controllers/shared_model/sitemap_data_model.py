from genesis.controllers.constants.strings import SITEMAP_STRINGS, GENERAL_STRINGS


class sitemap_data_model:
    def __init__(self):
        self.m_url = None
        self.m_email = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_name = None
        self.m_keyword = None
        self.m_secret_key = None
        self.m_submission_rule = SITEMAP_STRINGS.S_SITEMAP_SUBMISSION_RULE_1
        self.m_agreement = []

    def set_defaults(self):
        self.m_url = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_email = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_name = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_keyword = GENERAL_STRINGS.S_GENERAL_EMPTY
