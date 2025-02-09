
from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .category import SeaRecreationCategoryView
from .main import SeaRecreationView


def mount_sea_recreation_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        SeaRecreationView(
            db.SeaRecreation, session,
            category="Морской отдых",
            name="Точки отдыха"
        )
    )
    admin_app.add_view(
        SeaRecreationCategoryView(
            db.SeaRecreationCategory, session,
            category="Морской отдых",
            name="Категории"
        )
    )
