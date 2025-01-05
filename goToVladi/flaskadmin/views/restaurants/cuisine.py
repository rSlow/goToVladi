from goToVladi.flaskadmin.views.base import AppModelView


class RestaurantCuisineView(AppModelView):
    form_columns = ["name"]
    column_labels = {
        "name": "Вид кухни",
    }
