from flask_admin.contrib.sqla import ModelView

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.media import MediaInline


class TripView(ModelView):
    page_size = 10
    inline_models = [
        MediaInline(db.TripMedia),
    ]
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "site_url": "Сайт",
        "medias": "Медиафайлы",
        "region": "Город / регион",
    }
    column_list = ["region", "name"]
    column_filters = column_list
