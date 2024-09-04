from fastapi import FastAPI

from . import auth
from . import user


def setup_routes(app: FastAPI):
    app.include_router(auth.routes.setup())
    app.include_router(user.routes.setup())
