from wtforms.fields import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class BreakfastView(AppModelView,
                    DescriptionMixin,
                    ColumnListEqualFiltersMixin,
                    MediaFilesMixin[db.BreakfastMedia]):
    column_labels = {
        "name": "Название",
        "average_check": "Средний чек",
        "rating": "Рейтинг",
        "description": "Описание",
        "phone": "Телефон",
        "medias": "Медиафайлы",
        "region": "Город / регион",
        "regions": "Город",
    }
    column_filters = ["region", "name", "rating"]
    form_overrides = {"phone": TelField}
