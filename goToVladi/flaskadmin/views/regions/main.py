from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView


class RegionView(AppModelView):
    column_labels = {
        db.Region.name: "Название"
    }
