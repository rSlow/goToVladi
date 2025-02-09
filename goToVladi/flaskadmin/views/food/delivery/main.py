from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class DeliveryView(AppModelView,
                   DescriptionMixin,
                   ColumnListEqualFiltersMixin,
                   MediaFilesMixin[db.DeliveryMedia]):
    column_labels = {
        "name": "Название",
        "average_check": "Средний чек",
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
    column_filters = ["region", "name", "rating", "cuisine"]
    form_overrides = {"phone": TelField}
