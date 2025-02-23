from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class BarView(AppModelView,
              DescriptionMixin,
              MediaFilesMixin[db.BarMedia]):
    column_labels = {
        db.Bar.name: "Название",
        db.Bar.average_check: "Средний чек",
        db.Bar.rating: "Рейтинг",
        db.Bar.description: "Описание",
        db.Bar.phone: "Телефон",
        db.Bar.medias: "Медиафайлы",
        db.Bar.region: "Город / регион",
        "regions": "Город",
    }
    column_filters = ["region", "name", "rating"]
    form_overrides = {"phone": TelField}
