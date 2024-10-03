from flask_admin.contrib.sqla import ModelView


class HotelDistrictView(ModelView):
    column_labels = {
        "name": "Название района",
        "region": "Регион / город"
    }
    form_excluded_columns = ["hotels"]
