import re
from .enums.fields import DBFields, APIFields

URL_SHORT_DEFAULT_LENGTH = 6
URL_SHORT_MAX_LENGTH = 16

REGEX_PATTERNS = {
    'link_short_id': re.compile(r'^[a-zA-Z0-9]+$'),
}

ERROR_MESSAGES = {
    'invalid_short_link': 'Указано недопустимое имя для короткой ссылки',
    'duplicate_short_link': ('Предложенный вариант короткой ссылки '
                             'уже существует.'),
    'max_short_link_length': ('Короткая ссылка должна содержать '
                              'не более 16 символов'),
    'missing_request_body': 'Отсутствует тело запроса',
    'missing_url_field': '"url" является обязательным полем!',
    'invalid_id': 'Указанный id не найден',
}

FIELD_MAPPING = {
    APIFields.REQUEST_URL.value: DBFields.ORIGINAL.value,
    APIFields.REQUEST_CUSTOM_ID.value: DBFields.SHORT.value,
}

ROUTE_VARIABLES = {
    'short_id': '<string:short_id>',
}

INDEX_VIEW_NAME = 'index_view'
