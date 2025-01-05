from goToVladi.flaskadmin.views.base import AppModelView


class RegionView(AppModelView):
    column_labels = {
        "name": "Название"
    }
