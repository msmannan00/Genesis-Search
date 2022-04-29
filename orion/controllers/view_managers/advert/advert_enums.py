import enum


class ADVERT_MODEL_COMMANDS(enum.Enum):
    M_FETCH_ADVERT = 1


class ADVERT_SESSION_COMMANDS(enum.Enum):
    M_INIT = 1
    M_VALIDATE = 2
