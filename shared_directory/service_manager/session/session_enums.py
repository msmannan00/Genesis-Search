import enum


class SESSION_KEYS:
    S_USERNAME = "m_username"
    S_PASSWORD = "m_password"
    S_ROLE = "m_role"

class SESSION_COMMANDS(enum.Enum):
    S_CREATE = 1
    S_EXISTS = 2
    S_FETCH_USER = 3
