from goToVladi.core.data.db import models as db

from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class HotelView(AppModelView,
                DescriptionMixin,
                ColumnListEqualFiltersMixin,
                MediaFilesMixin[db.HotelMedia]):
    column_labels = {
        "name": "Название",
        "district": "Район",
        "site_url": "Сайт",
        "description": "Описание",
        "medias": "Медиафайлы",
        "min_price": "Минимальная цена",
        "promo_code": "Промокод",
        "hotel_districts": "Район",
    }
    column_filters = ["district", "name"]
