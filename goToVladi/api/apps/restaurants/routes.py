from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile, Path
from fastapi import Depends as fDepends

from goToVladi.api.apps.restaurants.forms import RestaurantInputForm
from goToVladi.core.data.db.dao import RestaurantDao


@inject
async def add_restaurant(
        dao: FromDishka[RestaurantDao],
        restaurant_form: RestaurantInputForm = fDepends(),
):
    restaurant_model = restaurant_form.to_model()
    restaurant_db = await dao.add(restaurant_model)
    return restaurant_db


@inject
async def add_media(
        dao: FromDishka[RestaurantDao],
        medias: list[UploadFile],
        id_: int = Path(alias="id"),
):
    res = await dao.add_medias(id_, *medias)
    return {"ok": res}


@inject
async def get_restaurant(
        dao: FromDishka[RestaurantDao],
        id_: int = Path(alias="id"),
):
    restaurant = await dao.get(id_)
    return restaurant


@inject
async def delete_restaurant(
        dao: FromDishka[RestaurantDao],
        id_: int = Path(alias="id"),
):
    await dao.delete(id_)
    return {"ok": True}


def setup():
    router = APIRouter(prefix="/restaurants", tags=["restaurants"])

    router.add_api_route("/", add_restaurant, methods=["POST"])
    router.add_api_route("/{id}/", get_restaurant, methods=["GET"])
    router.add_api_route("/{id}/", delete_restaurant, methods=["DELETE"])
    router.add_api_route("/{id}/media/", add_media, methods=["POST"])

    return router
