import enum


class USER_AUTH_COMMANDS(enum.Enum):
    M_INIT = 1
    M_AUTHENTICATE = 2
    M_LOGOUT = 3

class USER_AUTH_PARAM:
    M_USERNAME = "pUsername"
    M_PASSWORD = "pPassword"

class USER_DATA:
    M_DEFAULT_USERNAME = "admin"
