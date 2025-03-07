__all__ = [
    "mount_users_views"
]

from flask import flash
from flask_admin import Admin
from flask_admin.actions import action
from flask_login import current_user
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin import crud
from goToVladi.flaskadmin.views.base import AppModelView


class UserView(AppModelView):
    page_size = 20
    can_delete = False
    can_create = False
    column_labels = {
        db.User.tg_id: "Telegram ID",
        db.User.first_name: "Имя",
        db.User.last_name: "Фамилия",
        db.User.username: "Имя пользователя",
        db.User.is_superuser: "Администратор",
        db.User.region: "Город / регион",
    }
    column_filters = ["tg_id", "username", "is_superuser"]
    form_excluded_columns = [
        "hashed_password", "is_bot", "is_active",
        "created_at", "edited_at"
    ]
    form_widget_args = {
        "tg_id": {
            'readonly': True,
        },
    }

    @action(
        name="set_as_admin",
        text="Сделать администратором",
        confirmation="Вы действительно хотите дать этим пользователям права администратора?"
    )
    def set_as_admin(self, id_list: list[str]):
        id_list = [*map(int, id_list)]
        crud.user.set_admin_rights(self.session, id_list, True)
        flash(f"Обновлены права {len(id_list)} пользователям.", "info")

    @action(
        name="set_as_not_admin",
        text="Убрать права администратора",
        confirmation="Вы действительно забрать у этих пользователей права администратора?"
    )
    def set_as_not_admin(self, id_list: list[str]):
        id_list = [*map(int, id_list)]
        if current_user.id in id_list:
            id_list.remove(current_user.id)
            flash("Не убирайте права у себя :)", "warning")
        if id_list:
            crud.user.set_admin_rights(self.session, id_list, False)
            flash(f"Обновлены права {len(id_list)} пользователям.", "info")


def mount_users_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        UserView(
            db.User, session,
            name="Пользователи",
        ),
    )
