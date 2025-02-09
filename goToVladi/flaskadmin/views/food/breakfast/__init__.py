from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .main import BreakfastView


def mount_breakfast_view(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        BreakfastView(
            db.Breakfast, session,
            category="Гид по еде",
            name="Завтраки"
        )
    )
