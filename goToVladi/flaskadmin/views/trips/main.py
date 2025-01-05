from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.media_inline import MediaInline

from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class TripView(AppModelView,
               DescriptionMixin,
               ColumnListEqualFiltersMixin,
               MediaFilesMixin[db.RestaurantMedia]):
    inline_models = [
        MediaInline(db.TripMedia),
    ]
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "site_url": "Сайт",
        "medias": "Медиафайлы",
        "region": "Город / регион",
        "regions": "Город",
    }
    column_list = ["region", "name"]
