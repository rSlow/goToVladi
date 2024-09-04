from fastapi import FastAPI
from . import auth


def setup_routes(app: FastAPI):
    app.include_router(auth.routes.setup())
