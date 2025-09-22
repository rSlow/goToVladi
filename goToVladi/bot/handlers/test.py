import aiohttp
from aiogram import types, Router, Bot
from aiogram.filters import Command

from dialog_schematic_manager import DialogSchematicManager

message_json = {
    "chat_ids": [
        "959148697"
    ],
    "text": "some text",
    "button_factory": "INLINE",
    "keyboard": [
        [
            {
                "type_name": "url",
                "text": "URL-1",
                "url": "https://www.youtube.com/watch?v=7jN9T3500MM"
            },
        ],
        [
            {
                "type_name": "switch_state",
                "text": "SWITCH-MAIN",
                "state": "MainMenuSG:aa78c1d01",
                "start_data": [
                    {
                        "param_name": "start_param_1",
                        "param_value": "123"
                    },
                    {
                        "param_name": "start_param_2",
                        "param_value": "456"
                    },
                ],
                "dialog_data": [
                    {
                        "param_name": "dialog_param_3",
                        "param_value": "789"
                    },
                ]
            },
            {
                "type_name": "url",
                "text": "URL-2",
                "url": "https://www.youtube.com/watch?v=95Mkwbsk2HQ"
            },

        ],
        [
            {
                "type_name": "switch_state",
                "text": "SWITCH-HOTEL",
                "state": "HotelSG:hotel",
                "dialog_data": [
                    {
                        "param_name": "hotel_id",
                        "param_value": "1"
                    },
                ]
            },
        ]
    ]
}


async def cmd_test(message: types.Message, schematic_manager: DialogSchematicManager, bot:Bot):
    async with aiohttp.ClientSession() as session:
        res = await session.get(
            url=
        )
        schematic = await res.json()
        await message.answer(text=str(schematic))


def setup():
    router = Router(name=__name__)

    router.message.register(cmd_test, Command("test_msg"))

    return router
