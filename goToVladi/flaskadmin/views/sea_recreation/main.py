from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class SeaRecreationView(AppModelView,
                        DescriptionMixin,
                        ColumnListEqualFiltersMixin,
                        MediaFilesMixin[db.SeaRecreationMedia]):
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "region": "Город / регион",
        "category": "Категория",
        "rating": "Рейтинг",
        "phone": "Телефон",
    }
    column_filters = ["category", "name", "rating"]
    form_overrides = {"phone": TelField}
