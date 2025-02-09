from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile, Path
from fastapi import Depends as fDepends

from goToVladi.api.apps.hotels.forms import HotelInputForm
from goToVladi.core.data.db.dao import HotelDao


@inject
async def add_hotel(
        dao: FromDishka[HotelDao],
        hotel_form: HotelInputForm = fDepends(),
):
    hotel_model = hotel_form.to_model()
    return await dao.add(hotel_model)


@inject
async def add_media(
        dao: FromDishka[HotelDao],
        medias: list[UploadFile],
        id_: int = Path(alias="id"),
):
    res = await dao.add_medias(id_, *medias)
    return {"ok": res}


@inject
async def get_hotel(
        dao: FromDishka[HotelDao],
        id_: int = Path(alias="id"),
):
    hotel = await dao.get(id_)
    return hotel


@inject
async def delete_hotel(
        dao: FromDishka[HotelDao],
        id_: int = Path(alias="id"),
):
    await dao.delete(id_)
    return {"ok": True}


def setup():
    router = APIRouter(prefix="/hotels", tags=["hotels"])

    router.add_api_route("/", add_hotel, methods=["POST"])
    router.add_api_route("/{id}/", get_hotel, methods=["GET"])
    router.add_api_route("/{id}/", delete_hotel, methods=["DELETE"])
    router.add_api_route("/{id}/media/", add_media, methods=["POST"])

    return router
