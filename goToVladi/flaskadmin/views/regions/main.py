from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class RegionView(SecureModelView):
    column_labels = {
        "name": "Название"
    }
