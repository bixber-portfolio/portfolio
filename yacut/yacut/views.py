from flask import flash, redirect, render_template, url_for

from . import app
from .constants import ERROR_MESSAGES, ROUTE_VARIABLES, INDEX_VIEW_NAME
from .enums.message_types import FlashTypes
from .enums.fields import DBFields
from .forms import URLForm
from .models import URLMap
from .utils import create_and_get_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        data = {DBFields.ORIGINAL.value: form.original_link.data,
                DBFields.SHORT.value: form.custom_id.data}
        url_map = create_and_get_url(data)
        if url_map:
            if url_map.is_duplicate_short_id():
                flash(ERROR_MESSAGES.get('duplicate_short_link'),
                      FlashTypes.ERROR.value)
                return redirect(url_for(INDEX_VIEW_NAME))
            url_map.save_to_database()
            flash('Ваша новая ссылка готова:', FlashTypes.INFO.value)
            flash(url_map.get_short_url(), FlashTypes.LINK.value)
    return render_template('index.html',
                           form=form,
                           categories=[member.value for member in FlashTypes])


@app.route(f'/{ROUTE_VARIABLES["short_id"]}')
def redirect_to_original(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
