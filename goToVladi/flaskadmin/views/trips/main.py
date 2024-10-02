from flask_admin.contrib.sqla import ModelView

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.trips.media import MediaInline


class TripView(ModelView):
    inline_models = [
        MediaInline(db.TripMedia)
    ]
