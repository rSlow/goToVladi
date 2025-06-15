from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.fields import NoReadonlyCreateView


class MessageTextView(NoReadonlyCreateView, AppModelView):
    can_delete = False
    column_labels = {
        db.MessageText.name: "Ключ поля",
        db.MessageText.description: "Описание",
        db.MessageText.value: "Текст",
    }
    form_widget_args = {
        "name": {
            "readonly": True,
        },
    }
    column_filters = ["description", "value"]
