from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class RestaurantCuisineView(SecureModelView):
    form_columns = ["name"]
    column_labels = {
        "name": "Вид кухни",
    }
