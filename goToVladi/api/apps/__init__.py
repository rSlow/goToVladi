from fastapi import FastAPI

from . import auth, user, static, restaurants, hotels


def setup_routes(app: FastAPI):
    app.include_router(auth.routes.setup())
    app.include_router(user.routes.setup())
    app.include_router(static.routes.setup())

    app.include_router(restaurants.routes.setup())
    app.include_router(hotels.routes.setup())
