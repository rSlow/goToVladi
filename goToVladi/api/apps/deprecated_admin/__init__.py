from dishka import AsyncContainer
from fastadmin import fastapi_app as fastadmin_app
from fastapi import FastAPI

from .models import register_models
from .ulits.inject_context import AdminInjectContext


async def mount_admin_app(app: FastAPI, dishka: AsyncContainer):
    await register_models(dishka)

    AdminInjectContext.container = dishka
    # for inject in `authenticate_user()` in classSqlAlchemyModelAdmin

    app.mount(path=f"/admin", app=fastadmin_app)
