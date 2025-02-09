__all__ = [
    "mount_bar_view"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .main import BarView


def mount_bar_view(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        BarView(
            db.Bar, session,
            category="Гид по еде",
            name="Бары"
        )
    )
