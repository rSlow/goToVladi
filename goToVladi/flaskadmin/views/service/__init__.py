from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .message_text import MessageTextView
from .settings import SettingsView


def mount_service_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        MessageTextView(
            db.MessageText,
            session=session,
            name="Редактирование текстов",
            category="Служебное"
        )
    )
    admin_app.add_view(
        SettingsView(
            db.Setting,
            session=session,
            name="Ключи настроек",
            category="Служебное"
        )
    )
