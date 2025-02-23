from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class BreakfastView(AppModelView,
                    DescriptionMixin,
                    MediaFilesMixin[db.BreakfastMedia]):
    column_labels = {
        db.Breakfast.name: "Название",
        db.Breakfast.average_check: "Средний чек",
        db.Breakfast.rating: "Рейтинг",
        db.Breakfast.description: "Описание",
        db.Breakfast.phone: "Телефон",
        db.Breakfast.medias: "Медиафайлы",
        db.Breakfast.region: "Город / регион",
        "regions": "Город",
    }
    column_filters = ["region", "name", "rating"]
    form_overrides = {"phone": TelField}
