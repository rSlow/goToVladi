from flask_admin import Admin, expose
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin


class MessageTextView(AppModelView,
                      ColumnListEqualFiltersMixin):
    can_delete = False
    column_labels = {
        "name": "Ключ поля",
        "description": "Описание",
        "value": "Текст",
    }
    form_widget_args = {
        "name": {
            "readonly": True,
        },
    }
    column_filters = ["description", "value"]

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        args_to_return_readonly: list[str] = []
        for field_name, args in self.form_widget_args.items():
            if args.get("readonly") is True:
                args["readonly"] = False
                args_to_return_readonly.append(field_name)
        view = super(MessageTextView, self).create_view()
        for field_name in args_to_return_readonly:
            self.form_widget_args[field_name]["readonly"] = True
        return view


def mount_message_text_view(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        MessageTextView(
            db.MessageText,
            session=session,
            name="Редактирование текстов",
            category="Служебное"
        )
    )
