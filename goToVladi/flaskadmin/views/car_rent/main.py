from functools import partial

from wtforms import widgets
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class AgeField(DecimalField):
    widget = widgets.NumberInput(min=0, step=0.5)


class CarRentView(AppModelView,
                  DescriptionMixin,
                  MediaFilesMixin[db.CarRentMedia]):
    column_labels = {
        db.CarRent.car_classes: "Классы автомобилей",
        db.CarRent.region: "Город / регион",
        db.CarRent.name: "Название",
        db.CarRent.description: "Описание",
        db.CarRent.rating: "Рейтинг",
        db.CarRent.min_age: "Минимальный возраст",
        db.CarRent.min_experience: "Минимальный стаж",
        db.CarRent.min_price: "Минимальная цена",
        db.CarRent.phone: "Телефон",
        db.CarRent.site_url: "Сайт",
        "regions": "Город",
    }
    column_filters = ["name"]
    form_overrides = {
        "phone": TelField,
        "min_experience": partial(AgeField, places=1),
    }
