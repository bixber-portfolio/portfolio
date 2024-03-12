import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    ERROR_MESSAGES,
    REGEX_PATTERNS,
    ROUTE_VARIABLES,
    URL_SHORT_MAX_LENGTH,
)
from .error_handlers import InvalidAPIUsage
from .enums.fields import APIFields
from .models import URLMap


@app.route(f'/api/id/{ROUTE_VARIABLES["short_id"]}/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            ERROR_MESSAGES.get('invalid_id'),
            HTTPStatus.NOT_FOUND,
        )
    return jsonify(
        {APIFields.REQUEST_URL.value: url_map.original}
    ), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(ERROR_MESSAGES.get('missing_request_body'))

    original_link = data.get(APIFields.REQUEST_URL.value)
    short_id = data.get(APIFields.REQUEST_CUSTOM_ID.value)
    if not original_link:
        raise InvalidAPIUsage(ERROR_MESSAGES.get('missing_url_field'))
    if not short_id:
        data[APIFields.REQUEST_CUSTOM_ID.value] = URLMap.get_unique_short_id()
    elif (
        not re.search(REGEX_PATTERNS['link_short_id'], short_id)
        or len(short_id) > URL_SHORT_MAX_LENGTH
    ):
        raise InvalidAPIUsage(ERROR_MESSAGES.get('invalid_short_link'))
    elif URLMap.is_existence_short_id(short_id):
        raise InvalidAPIUsage(ERROR_MESSAGES.get('duplicate_short_link'))
    url_map = URLMap()
    url_map.from_dict(data)
    url_map.save_to_database()
    response_data = {
        APIFields.RESPONSE_URL.value: url_map.original,
        APIFields.RESPONSE_SHORT_LINK.value: url_map.get_short_url(),
    }
    return jsonify(response_data), HTTPStatus.CREATED
