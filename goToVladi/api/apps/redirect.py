from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.utils import dates


@inject
async def redirect_to(
        dao: FromDishka[DaoHolder],
        url: Annotated[AnyUrl, Query()],
        chat_id: Annotated[int, Query()], user_id: Annotated[int, Query()],
        data: Annotated[str, Query()] | None = None,
):
    event = dto.LogEvent(
        type_="url",
        chat_id=chat_id,
        user_id=user_id,
        data=data,
        dt=dates.get_now(dates.tz_utc)
    )
    await dao.log.write_event(event)
    return RedirectResponse(url=str(url))  # TODO quote


def setup():
    router = APIRouter(prefix="/redirect")

    router.add_api_route("/", redirect_to, methods=["GET"])

    return router
