from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.views.food.cuisine import FoodCuisineView
from . import restaurants, delivery, bar, breakfast


def mount_food_view(admin_app: Admin, session: scoped_session[Session]):
    restaurants.mount_restaurant_view(admin_app, session)
    delivery.mount_delivery_view(admin_app, session)
    bar.mount_bar_view(admin_app, session)
    breakfast.mount_breakfast_view(admin_app, session)

    admin_app.add_view(
        FoodCuisineView(
            db.FoodCuisine, session,
            category="Гид по еде",
            name="Кухни",
        )
    )
