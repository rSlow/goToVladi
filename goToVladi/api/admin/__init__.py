from dishka import AsyncContainer
from fastadmin import fastapi_app as fastadmin_app
from fastapi import FastAPI

from goToVladi.api.admin.models import register_models
from goToVladi.api.config.models import ApiAppConfig


async def mount_admin_app(
        app: FastAPI, dishka: AsyncContainer, config: ApiAppConfig
):
    await register_models(dishka)
    app.mount(path=f"/{config.admin.ADMIN_PREFIX}", app=fastadmin_app)
