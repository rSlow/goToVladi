from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class SeaRecreationView(AppModelView,
                        DescriptionMixin,
                        MediaFilesMixin[db.SeaRecreationMedia]):
    column_labels = {
        db.SeaRecreation.name: "Название",
        db.SeaRecreation.description: "Описание",
        db.SeaRecreation.region: "Город / регион",
        db.SeaRecreation.category: "Категория",
        db.SeaRecreation.rating: "Рейтинг",
        "phone": "Телефон",
    }
    column_filters = ["category", "name", "rating"]
    form_overrides = {"phone": TelField}
