from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class HotelDistrictView(SecureModelView):
    column_labels = {
        "name": "Название района",
        "region": "Регион / город"
    }
    form_excluded_columns = ["hotels"]
