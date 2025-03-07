from fastapi import FastAPI

from goToVladi.api.config.models import ApiAppConfig
from . import auth, user, media, restaurants, hotels, redirect


def setup_routes(app: FastAPI, config: ApiAppConfig):
    app.include_router(auth.routes.setup())
    app.include_router(user.routes.setup())
    app.include_router(redirect.setup())

    app.include_router(restaurants.routes.setup())
    app.include_router(hotels.routes.setup())

    if config.api.debug is True:
        app.include_router(media.routes.setup(config))
