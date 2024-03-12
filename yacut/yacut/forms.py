from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Optional

from .validators import custom_id_validator


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка', validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Значение должно быть ссылкой'),
        ]
    )
    custom_id = URLField(
        'Короткий id ссылки (необязательно)',
        validators=[Optional(), custom_id_validator],
    )
    submit = SubmitField('Создать')