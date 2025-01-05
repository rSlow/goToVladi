__all__ = [
    "mount_restaurant_views"
]

from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from .main import RestaurantView
from .cuisine import RestaurantCuisineView


def mount_restaurant_views(admin_app: Admin, session: scoped_session[Session]):
    admin_app.add_view(
        RestaurantView(
            db.Restaurant, session,
            category="Рестораны",
            name="Рестораны"
        )
    )
    admin_app.add_view(
        RestaurantCuisineView(
            db.RestaurantCuisine, session,
            category="Рестораны",
            name="Кухни",
        )
    )
