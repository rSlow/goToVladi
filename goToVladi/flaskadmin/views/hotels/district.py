from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin

from goToVladi.core.data.db import models as db


class HotelDistrictView(ModelView):
    inline_models = [
        InlineFormAdmin(db.Hotel)
    ]
