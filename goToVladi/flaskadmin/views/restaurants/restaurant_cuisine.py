from flask_admin.contrib.sqla import ModelView


class RestaurantCuisineView(ModelView):
    form_columns = ["name"]
    column_labels = {
        "name": "Вид кухни",
    }

