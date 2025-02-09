from goToVladi.flaskadmin.views.base import AppModelView


class SeaRecreationCategoryView(AppModelView):
    column_labels = {
        "name": "Вид",
    }
    # form_excluded_columns = ["sea_recreations"]
