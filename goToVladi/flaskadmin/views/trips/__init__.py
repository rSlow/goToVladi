__all__ = [
    "mount_trips_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.trips.main import TripView


def mount_trips_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        TripView(
            db.Trip, session,
            category="Экскурсии",
            name="Экскурсии"
        )
    )
