__all__ = [
    "mount_car_rent_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .car_classes import CarClassView
from .main import CarRentView


def mount_car_rent_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        CarRentView(
            db.CarRent, session,
            category="Автопрокаты",
            name="Автопрокаты"
        )
    )
    admin_app.add_view(
        CarClassView(
            db.CarClass, session,
            category="Автопрокаты",
            name="Классы автомобилей"
        )
    )
