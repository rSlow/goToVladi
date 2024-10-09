__all__ = [
    "mount_users_views"
]

from flask import flash
from flask_admin import Admin
from flask_admin.actions import action
from flask_login import current_user
from sqlalchemy import update
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.utils.secure_view import SecureModelView


class UserView(SecureModelView):
    page_size = 20
    can_delete = False
    can_create = False
    column_labels = {
        "tg_id": "Telegram ID",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "username": "Имя пользователя",
        "is_superuser": "Администратор",
        "region": "Город / регион",
    }
    column_list = ["tg_id", "username", "is_superuser"]
    column_filters = column_list
    form_excluded_columns = [
        "hashed_password", "is_bot",
        "created_at", "edited_at"
    ]
    form_widget_args = {
        'tg_id': {
            'readonly': True,
        }
    }

    @action(
        name="set_as_admin",
        text="Сделать администратором",
        confirmation="Вы действительно хотите дать этим пользователям "
                     "права администратора?"
    )
    def set_as_admin(self, id_list: list[str]):
        id_list = [*map(int, id_list)]
        self._set_admin_rights(id_list, True)
        flash(f"Обновлены права {len(id_list)} пользователям.", "info")

    @action(
        name="set_as_not_admin",
        text="Убрать права администратора",
        confirmation="Вы действительно забрать у этих пользователей "
                     "права администратора?"
    )
    def set_as_not_admin(self, id_list: list[str]):
        id_list = [*map(int, id_list)]
        try:
            current_user_id_index = id_list.index(current_user.id)
            current_user_id = id_list.pop(current_user_id_index)
        except (IndexError, ValueError):
            current_user_id = None
        if current_user_id:
            flash("Не убирайте права у себя :)", "warning")
        if id_list:
            self._set_admin_rights(id_list, False)
            flash(f"Обновлены права {len(id_list)} пользователям.", "info")

    def _set_admin_rights(self, ids: list[int], is_superuser: bool) -> None:
        self.session.execute(
            update(db.User)
            .where(db.User.id.in_(ids))
            .values(is_superuser=is_superuser)
        )
        self.session.commit()


def mount_users_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        UserView(
            db.User, session,
            name="Пользователи"
        )
    )
