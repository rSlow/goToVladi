from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query, Body
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl

from bot_schema_parser import ApiMessage
from bot_schema_parser.schema_manager import BotSchemaManager
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import EventLogDao
from goToVladi.core.utils import dates


@inject
async def parse_bot_message(
        message: Annotated[ApiMessage, Body()],
        bot_schema_manager: FromDishka[BotSchemaManager],
):
    await bot_schema_manager.create_message(message)


def setup():
    router = APIRouter(prefix="/bot_message")

    router.add_api_route("/", parse_bot_message, methods=["POST"], status_code=200)

    return router
