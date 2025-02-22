from functools import partial

from wtforms import widgets
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class AgeField(DecimalField):
    widget = widgets.NumberInput(min=0, step=0.5)


class CarRentView(AppModelView,
                  DescriptionMixin,
                  ColumnListEqualFiltersMixin,
                  MediaFilesMixin[db.CarRentMedia]):
    column_labels = {
        "car_classes": "Классы автомобилей",
        "region": "Город / регион",
        "name": "Название",
        "description": "Описание",
        "rating": "Рейтинг",
        "min_age": "Минимальный возраст",
        "min_experience": "Минимальный стаж",
        "min_price": "Минимальная цена",
        "phone": "Телефон",
        "site_url": "Сайт",
        "medias": "Медиафайлы",
    }
    column_filters = ["name"]
    form_overrides = {
        "phone": TelField,
        "min_experience": partial(AgeField, places=1),
    }
