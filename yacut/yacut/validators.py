from wtforms.validators import Regexp

from .constants import REGEX_PATTERNS

custom_id_validator = Regexp(
    regex=REGEX_PATTERNS['link_short_id'],
    message=('Неверный формат короткого id. '
             'Допустимы буквы (русские и английские) и цифры.')
)