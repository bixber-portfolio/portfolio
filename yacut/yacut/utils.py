import re

from flask import flash

from .constants import ERROR_MESSAGES, REGEX_PATTERNS, URL_SHORT_MAX_LENGTH
from .enums.message_types import FlashTypes
from .models import URLMap


def create_and_get_url(data):
    short_id = data.get('short')
    if short_id:
        if len(short_id) > URL_SHORT_MAX_LENGTH:
            flash(
                ERROR_MESSAGES.get('max_short_link_length'),
                FlashTypes.ERROR.value,
            )
            return
        if re.search(REGEX_PATTERNS['link_short_id'], short_id) is None:
            flash(
                ERROR_MESSAGES.get('invalid_short_link'),
                FlashTypes.ERROR.value,
            )
            return
    else:
        data['short'] = URLMap.get_unique_short_id()
    url_map = URLMap(**data)
    return url_map
