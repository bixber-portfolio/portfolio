from enum import Enum


class APIFields(Enum):
    REQUEST_URL = 'url'
    REQUEST_CUSTOM_ID = 'custom_id'

    RESPONSE_URL = 'url'
    RESPONSE_SHORT_LINK = 'short_link'


class DBFields(Enum):
    ORIGINAL = 'original'
    SHORT = 'short'
