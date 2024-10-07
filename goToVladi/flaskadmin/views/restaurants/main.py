from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.fields.file import SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class RestaurantView(SecureModelView):
    page_size = 10
    inline_models = [
        MediaInline(db.RestaurantMedia)
    ]
    column_labels = {
        "name": "Название",
        "average_check": "Средний чек",
        "is_inner": "Можно внутри",
        "is_delivery": "Есть доставка",
        "rating": "Рейтинг",
        "priority": "Приоритет",
        "site_url": "Сайт",
        "description": "Описание",
        "phone": "Телефон",
        "medias": "Медиафайлы",
        "cuisine": "Кухня",
        "instagram": "Instagram",
        "vk": "ВК",
        "whatsapp": "Whatsapp",
        "telegram": "Telegram",
        "region": "Город / регион",
    }
    column_list = ["region", "name", "rating", "cuisine"]
    column_filters = column_list
    form_overrides = {"phone": TelField}
    form_extra_fields = {
        "multi_media": SQLAlchemyMultipleFileUploadField(
            field_name="medias", relation_class=db.RestaurantMedia,
            label="Загрузка медиафайлов"
        )
    }
    form_widget_args = {
        'description': {
            'rows': 8,
        }
    }
