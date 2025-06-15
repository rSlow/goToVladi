from dishka import FromDishka
from dishka.integrations.flask import inject
from flask_login import current_user

from goToVladi.core.config.models import AppConfig
from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.fields import NoReadonlyCreateView


class SettingsView(NoReadonlyCreateView, AppModelView):
    column_labels = {
        db.Setting.key: "Ключ поля",
        db.Setting.value: "Значение",
    }
    form_widget_args = {
        "key": {
            "readonly": True,
        },
    }
    column_filters = ["key", "value"]

    @inject
    def is_visible(self, app_config: FromDishka[AppConfig]):
        if current_user.is_authenticated:
            return current_user.tg_id in app_config.admins
