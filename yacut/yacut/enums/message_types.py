import enum


@enum.unique
class FlashTypes(enum.Enum):
    INFO = 'info'
    ERROR = 'error'
    LINK = 'link'