from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session, configure_mappers

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.restaurants import RestaurantCuisineView
from goToVladi.flaskadmin.views.restaurants import RestaurantView
from goToVladi.flaskadmin.views.trips.main import TripView


def mount_views(admin_app: Admin, session: scoped_session[Session]):
    configure_mappers()

    admin_app.add_view(
        TripView(
            db.Trip, session,
            category="Экскурсии", menu_class_name="Экскурсии"
        )
    )

    admin_app.add_view(
        RestaurantView(
            db.Restaurant, session,
            category="Рестораны"
        )
    )
    admin_app.add_view(
        RestaurantCuisineView(
            db.RestaurantCuisine, session,
            category="Рестораны"
        )
    )
