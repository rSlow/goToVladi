__all__ = [
    "mount_region_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .main import RegionView


def mount_region_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        RegionView(
            db.Region, session,
            # category="Регионы",
            name="Регионы"
        )
    )
