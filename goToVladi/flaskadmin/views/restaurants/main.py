from flask_admin.contrib.sqla import ModelView

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.trips.media import MediaInline


class RestaurantView(ModelView):
    page_size = 5
    column_list = ["name", "priority"]
    inline_models = [
        MediaInline(db.RestaurantMedia)
    ]
