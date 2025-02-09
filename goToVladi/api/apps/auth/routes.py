import typing
from typing import Annotated

from aiogram.types import User
from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter
from fastapi import Depends as fDepends, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse, Response

from goToVladi.api.utils.auth import AuthService
from goToVladi.api.utils.auth.cookie import set_auth_cookie
from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.core.config.models import SecurityConfig
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import UserDao
from goToVladi.core.utils.auth import TG_WIDGET_HTML
from goToVladi.core.utils.auth.models import UserTgAuth, WebAppAuth
from .utils.hash import check_tg_hash, check_webapp_hash


@inject
async def login(
        response: Response,
        auth_service: FromDishka[AuthService],
        security_config: FromDishka[SecurityConfig],
        dao: FromDishka[UserDao],
        form_data: OAuth2PasswordRequestForm = fDepends(),
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password, dao)
    token = auth_service.create_user_token(user)
    set_auth_cookie(security_config, response, token)
    return {"ok": True}


@inject
async def logout(
        response: Response,
        config: FromDishka[SecurityConfig],
):
    response.delete_cookie(
        "Authorization",
        samesite=config.samesite,
        domain=config.domain,
        httponly=config.httponly,
        secure=config.secure,
    )
    return {"ok": True}


@inject
async def tg_login_result(
        response: Response,
        user: Annotated[UserTgAuth, fDepends()],
        dao: FromDishka[UserDao],
        auth_service: FromDishka[AuthService],
        security_config: FromDishka[SecurityConfig],
        bot_config: FromDishka[BotConfig]
):
    check_tg_hash(user, bot_config.token)
    saved = await dao.upsert_user(user.to_dto())
    token = auth_service.create_user_token(saved)
    set_auth_cookie(security_config, response, token)
    return {"ok": True}


@inject
async def tg_login_result_post(
        response: Response,
        user: Annotated[UserTgAuth, Body()],
        dao: FromDishka[UserDao],
        auth_service: FromDishka[AuthService],
        security_config: FromDishka[SecurityConfig],
        bot_config: FromDishka[BotConfig]
):
    check_tg_hash(user, bot_config.token)
    saved_user = await dao.upsert_user(user.to_dto())
    token = auth_service.create_user_token(saved_user)
    set_auth_cookie(security_config, response, token)
    return {"ok": True}


@inject
async def webapp_login_result_post(
        response: Response,
        web_auth: Annotated[WebAppAuth, Body()],
        dao: FromDishka[UserDao],
        auth_service: FromDishka[AuthService],
        security_config: FromDishka[SecurityConfig],
        bot_config: FromDishka[BotConfig]
):
    parsed = check_webapp_hash(web_auth.init_data, bot_config.token)
    user = dto.User.from_aiogram(typing.cast(User, parsed.user))
    saved = await dao.upsert_user(user)
    token = auth_service.create_user_token(saved)
    set_auth_cookie(security_config, response, token)
    return {"ok": True}


@inject
async def tg_login_page(config: FromDishka[SecurityConfig]):
    return TG_WIDGET_HTML.format(
        bot_username=config.tg_bot_username,
        auth_url=config.domain + "/auth/login/data",
    )


def setup():
    router = APIRouter(prefix='/auth', tags=['auth'])

    router.add_api_route("/token", login, methods=["POST"])
    router.add_api_route("/login", tg_login_page, response_class=HTMLResponse, methods=["GET"])
    router.add_api_route("/logout", logout, methods=["POST"])

    router.add_api_route("/login/data", tg_login_result, methods=["GET"])
    router.add_api_route("/login/data", tg_login_result_post, methods=["POST"])

    router.add_api_route("/login/webapp", webapp_login_result_post, methods=["POST"])

    return router
