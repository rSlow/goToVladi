from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.secure_view import SecureModelView
from goToVladi.flaskadmin.utils.media_inline import MediaInline


class HotelView(SecureModelView):
    page_size = 10
    inline_models = [
        MediaInline(db.HotelMedia),
    ]
    column_labels = {
        "name": "Название",
        "district": "Район",
        "site_url": "Сайт",
        "description": "Описание",
        "medias": "Медиафайлы",
        "min_price": "Минимальная цена",
        "promo_code": "Промокод",
    }
    column_filters = ["district", "name"]
    column_list = column_filters
