from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView


class SeaRecreationCategoryView(AppModelView):
    column_labels = {
        db.SeaRecreationCategory: "Вид",
    }
    # form_excluded_columns = ["sea_recreations"]
