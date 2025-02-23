from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class MassageView(AppModelView,
                  DescriptionMixin,
                  MediaFilesMixin[db.MassageMedia]):
    column_labels = {
        db.Massage.name: "Название",
        db.Massage.description: "Описание",
        db.Massage.rating: "Рейтинг",
        db.Massage.phone: "Телефон",
        db.Massage.min_price: "Минимальная цена",
        db.Massage.region: "Город / регион",
        "regions": "Город",
    }
    column_filters = ["region", "name"]
    form_overrides = {"phone": TelField}
