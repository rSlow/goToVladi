from goToVladi.core.data.db import models as db

from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class HotelView(AppModelView,
                DescriptionMixin,
                MediaFilesMixin[db.HotelMedia]):
    column_labels = {
        db.Hotel.name: "Название",
        db.Hotel.district: "Район",
        db.Hotel.site_url: "Сайт",
        db.Hotel.description: "Описание",
        db.Hotel.medias: "Медиафайлы",
        db.Hotel.min_price: "Минимальная цена",
        db.Hotel.promo_code: "Промокод",
        "hotel_districts": "Район",
    }
    column_filters = ["district", "name"]
