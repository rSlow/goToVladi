from flask_admin.contrib.sqla.view import ModelView


class RegionView(ModelView):
    column_labels = {
        "name": "Название"
    }
