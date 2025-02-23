from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.base import AppModelView


class CooperationView(AppModelView):
    can_create = False
    column_labels = {
        db.Cooperation.text: "Текст",
        db.Cooperation.is_archived: "Архивное",
        db.Cooperation.created_at: "Время создания",
    }
    form_excluded_columns = ["edited_at"]
    column_exclude_list = form_excluded_columns
    column_filters = ["created_at", "is_archived"]


def mount_cooperation_view(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        CooperationView(
            db.Cooperation,
            session=session,
            name="Заявки на сотрудничество",
        )
    )
