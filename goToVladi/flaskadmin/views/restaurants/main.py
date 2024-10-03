from flask_admin.contrib.sqla import ModelView
from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.fields.multiple_file import \
    SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.views.media import MediaInline


class RestaurantView(ModelView):
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
