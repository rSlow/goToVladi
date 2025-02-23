from goToVladi.core.data.db import models as db

from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class TripView(AppModelView,
               DescriptionMixin,
               MediaFilesMixin[db.TripMedia]):
    column_labels = {
        db.Trip.name: "Название",
        db.Trip.description: "Описание",
        db.Trip.site_url: "Сайт",
        db.Trip.medias: "Медиафайлы",
        db.Trip.region: "Город / регион",
        "regions": "Город",
    }
    column_filters = ["region", "name"]
