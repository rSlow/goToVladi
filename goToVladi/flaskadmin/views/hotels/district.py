from goToVladi.flaskadmin.views.base import AppModelView


class HotelDistrictView(AppModelView):
    column_labels = {
        "name": "Название района",
        "region": "Регион / город"
    }
    form_excluded_columns = ["hotels"]
