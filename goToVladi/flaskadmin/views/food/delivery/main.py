from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class DeliveryView(AppModelView,
                   DescriptionMixin,
                   MediaFilesMixin[db.DeliveryMedia]):
    column_labels = {
        db.Delivery.name: "Название",
        db.Delivery.average_check: "Средний чек",
        db.Delivery.rating: "Рейтинг",
        db.Delivery.priority: "Приоритет",
        db.Delivery.site_url: "Сайт",
        db.Delivery.description: "Описание",
        db.Delivery.phone: "Телефон",
        db.Delivery.medias: "Медиафайлы",
        db.Delivery.cuisine: "Кухня",
        db.Delivery.instagram: "Instagram",
        db.Delivery.vk: "ВК",
        db.Delivery.whatsapp: "Whatsapp",
        db.Delivery.telegram: "Telegram",
        db.Delivery.region: "Город / регион",
        "restaurant_cuisines": "Кухня",
        "regions": "Город",
    }
    column_filters = ["region", "name", "rating", "cuisine"]
    form_overrides = {"phone": TelField}
