__all__ = [
    "mount_delivery_view"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .main import DeliveryView


def mount_delivery_view(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        DeliveryView(
            db.Delivery, session,
            category="Гид по еде",
            name="Доставки"
        )
    )
