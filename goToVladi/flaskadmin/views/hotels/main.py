from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.fields.multiple_file import \
    SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class HotelView(SecureModelView):
    page_size = 10
    inline_models = [
        MediaInline(db.HotelMedia),
    ]
    column_labels = {
        "name": "Название",
        "district": "Район",
        "site_url": "Сайт",
        "description": "Описание",
        "medias": "Медиафайлы",
        "min_price": "Минимальная цена",
        "promo_code": "Промокод",
    }
    column_filters = ["district", "name"]
    column_list = column_filters
    form_extra_fields = {
        "multi_media": SQLAlchemyMultipleFileUploadField(
            field_name="medias", relation_class=db.HotelMedia,
            label="Загрузка медиафайлов"
        )
    }
    form_widget_args = {
        'description': {
            'rows': 8,
        }
    }
