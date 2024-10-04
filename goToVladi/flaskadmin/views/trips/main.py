from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.secure_view import SecureModelView
from goToVladi.flaskadmin.utils.media_inline import MediaInline


class TripView(SecureModelView):
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
