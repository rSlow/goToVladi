__all__ = [
    "mount_massages_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.massages.main import MassageView


def mount_massages_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        MassageView(
            db.Massage, session,
            name="Спа / массажи"
        )
    )
