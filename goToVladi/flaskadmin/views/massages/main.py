from wtforms.fields.simple import TelField

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.media_inline import MediaInline
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.description import DescriptionMixin
from goToVladi.flaskadmin.views.mixins.media import MediaFilesMixin


class MassageView(AppModelView,
                  DescriptionMixin,
                  ColumnListEqualFiltersMixin,
                  MediaFilesMixin[db.MassageMedia]):
    inline_models = [
        MediaInline(db.MassageMedia),
    ]
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "rating": "Рейтинг",
        "phone": "Телефон",
        "min_price": "Минимальная цена",
        "region": "Город / регион",
        "regions": "Город",
    }
    column_list = ["region", "name"]
    form_overrides = {"phone": TelField}
