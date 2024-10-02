__all__ = [
    "mount_hotel_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .district import HotelDistrictView
from .main import HotelView


def mount_hotel_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        HotelView(
            db.Hotel, session,
            category="Отели",
            name="Отели"
        )
    )
    admin_app.add_view(
        HotelDistrictView(
            db.HotelDistrict, session,
            category="Отели",
            name="Районы отелей"
        )
    )
