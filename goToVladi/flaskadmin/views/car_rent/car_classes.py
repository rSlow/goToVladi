from flask_admin.model.form import InlineFormAdmin

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView


class CarRentModelForm(InlineFormAdmin):
    form_columns = ("id", "name", "region")


class CarClassView(AppModelView):
    inline_models = [
        # CarRentModelForm(db.CarRent)
    ]
    form_excluded_columns = ["car_rents"]
    column_labels = {
        db.CarClass.name: "Название",
        db.CarClass.description: "Описание",
        db.CarClass.car_rents: "Автопрокаты",
    }
