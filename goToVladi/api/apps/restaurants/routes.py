from dataclasses import dataclass
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile, Form, File, Path
from fastapi import Depends as fDepends

from goToVladi.core.data.db import forms
from goToVladi.core.data.db.dao import DaoHolder


@dataclass
class SimpleModel:
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]
    photo: Annotated[UploadFile, File()]
    file: Annotated[UploadFile, File()]


@inject
async def add_restaurant(
        dao: FromDishka[DaoHolder],
        restaurant_form: forms.RestaurantInputForm = fDepends(),
):
    restaurant_db = await dao.restaurant.add(restaurant_form)
    return restaurant_db


@inject
async def get_restaurant(
        dao: FromDishka[DaoHolder],
        id_: int = Path(alias="id"),
):
    restaurant = await dao.restaurant.get(id_)
    return restaurant


@inject
async def delete_restaurant(
        dao: FromDishka[DaoHolder],
        id_: int = Path(alias="id"),
):
    await dao.restaurant.delete(id_)
    return {"ok": True}


def setup():
    router = APIRouter(prefix="/restaurants", tags=["restaurants"])

    router.add_api_route("/", add_restaurant, methods=["POST"])
    router.add_api_route("/{id}/", get_restaurant, methods=["GET"])
    router.add_api_route("/{id}/", delete_restaurant, methods=["DELETE"])

    return router
