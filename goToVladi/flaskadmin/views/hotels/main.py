from flask_admin.contrib.sqla import ModelView

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.media import MediaInline


class HotelView(ModelView):
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
