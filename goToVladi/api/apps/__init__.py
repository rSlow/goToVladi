from fastapi import FastAPI

from goToVladi.api.config.models import ApiAppConfig
from . import auth, user, static, restaurants, hotels


def setup_routes(app: FastAPI, config: ApiAppConfig):
    app.include_router(auth.routes.setup())
    app.include_router(user.routes.setup())
    app.include_router(static.routes.setup(config))

    app.include_router(restaurants.routes.setup())
    app.include_router(hotels.routes.setup())
