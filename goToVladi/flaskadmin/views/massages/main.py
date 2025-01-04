from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.fields.file import SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class MassageView(SecureModelView):
    page_size = 10  # TODO сделать mixin?
    inline_models = [
        MediaInline(db.MassageMedia),
    ]
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "rating": "Рейтинг",
        "phone": "Телефон",
        "min_price": "Минимальная цена",
        "medias": "Медиафайлы",
        "region": "Город / регион",
        "regions": "Город",
    }
    column_list = ["region", "name"]
    column_filters = column_list  # TODO сделать mixin?
    form_overrides = {"phone": TelField}
    form_extra_fields = {  # TODO сделать mixin?
        "multi_media": SQLAlchemyMultipleFileUploadField(
            field_name="medias", relation_class=db.MassageMedia,
            label="Загрузка медиафайлов"
        )
    }
    form_widget_args = {  # TODO сделать mixin?
        'description': {
            'rows': 8,
        }
    }
