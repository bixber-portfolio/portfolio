import random
import string
from datetime import datetime

from flask import url_for

from . import db
from .constants import FIELD_MAPPING, URL_SHORT_DEFAULT_LENGTH, INDEX_VIEW_NAME


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def is_duplicate_short_id(self):
        return __class__.query.filter_by(short=self.short).first() is not None

    def from_dict(self, data):
        for api_field, db_field in FIELD_MAPPING.items():
            if api_field in data:
                setattr(self, db_field, data[api_field])

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def get_short_url(self):
        full_url = url_for(INDEX_VIEW_NAME, _external=True)
        return f'{full_url}{self.short}'

    @classmethod
    def is_existence_short_id(cls, short_id):
        return cls.query.filter_by(short=short_id).first() is not None

    @staticmethod
    def get_unique_short_id(length=URL_SHORT_DEFAULT_LENGTH):
        characters = string.ascii_letters + string.digits
        while True:
            shortened_url = ''.join(
                random.choice(characters) for _ in range(length)
            )
            if not URLMap.query.filter_by(short=shortened_url).first():
                return shortened_url
