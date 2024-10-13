from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.fields.file import SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class TripView(SecureModelView):
    page_size = 10
    inline_models = [
        MediaInline(db.TripMedia),
    ]
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "site_url": "Сайт",
        "medias": "Медиафайлы",
        "region": "Город / регион",
        "regions": "Город",
    }
    column_list = ["region", "name"]
    column_filters = column_list
    form_extra_fields = {
        "multi_media": SQLAlchemyMultipleFileUploadField(
            field_name="medias", relation_class=db.TripMedia,
            label="Загрузка медиафайлов"
        )
    }
    form_widget_args = {
        'description': {
            'rows': 8,
        }
    }
