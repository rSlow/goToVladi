from aiogram import types, Router
from aiogram.filters import Command

from bot_schema_parser import ApiMessage
from bot_schema_parser.schema_manager import BotSchemaManager
from bot_schema_parser.types import MANAGER_KEY

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


async def cmd_test(_message: types.Message, **kwargs):
    schema_manager: BotSchemaManager = kwargs.get(MANAGER_KEY)
    api_message = ApiMessage.model_validate(message_json)
    await schema_manager.handle_message(api_message)


def setup():
    router = Router(name=__name__)

    router.message.register(cmd_test, Command("test_msg"))

    return router
