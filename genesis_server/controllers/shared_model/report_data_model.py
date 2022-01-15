from genesis_server.controllers.constants.strings import GENERAL_STRINGS


class report_data_model:
    def __init__(self):
        self.m_url = None
        self.m_email = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_message = None

    def set_defaults(self):
        self.m_url = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_email = GENERAL_STRINGS.S_GENERAL_EMPTY
        self.m_message = GENERAL_STRINGS.S_GENERAL_EMPTY
