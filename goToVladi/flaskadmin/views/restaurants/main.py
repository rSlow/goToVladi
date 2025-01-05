from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class RestaurantView(AppModelView,
                     DescriptionMixin,
                     ColumnListEqualFiltersMixin,
                     MediaFilesMixin[db.RestaurantMedia]):
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
        "restaurant_cuisines": "Кухня",
        "regions": "Город",
    }
    column_list = ["region", "name", "rating", "cuisine"]
    form_overrides = {"phone": TelField}
