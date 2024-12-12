import logging

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path

from goToVladi.api.utils.auth import AuthService
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder

logger = logging.getLogger(__name__)


@inject
async def read_users_me(current_user: FromDishka[dto.User]) -> dto.User:
    return current_user


@inject
async def read_user(
        dao: FromDishka[DaoHolder],
        id_: int = Path(alias="id")
) -> dto.User:
    return await dao.user.get_by_id(id_)


@inject
async def set_password_route(
        auth_service: FromDishka[AuthService],
        user: FromDishka[dto.User],
        dao: FromDishka[DaoHolder],
        password: str = Body()
):
    await auth_service.update_user_password(user, password, dao)
    raise HTTPException(status_code=200)


def setup() -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    router.add_api_route("/me", read_users_me, methods=["GET"], response_model=dto.User)
    router.add_api_route("/me/password", set_password_route, methods=["PUT"])
    router.add_api_route("/{id}", read_user, methods=["GET"])

    return router
