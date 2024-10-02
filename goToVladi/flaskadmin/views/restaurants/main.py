from flask_admin.contrib.sqla import ModelView

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.media import MediaInline


class RestaurantView(ModelView):
    page_size = 5
    column_list = ["name", "priority"]
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
