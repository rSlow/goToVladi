from aiogram import Dispatcher

from .attrs import MANAGER_KEY
from .collector import get_dialog_schematic
from .dialog_manager import DialogSchematicManager


def setup_schema(
        dp: Dispatcher,
        # bot: Bot,
        # data_builder: BaseDataBuilder,
        # *buttons_to_register: ApiButton,
        # send_executor: SendExecutor | None = None,
)-> DialogSchematicManager:
    # bot_schema: BotSchema = get_dp_schematic(dp)
    # bot_button_manager = BotButtonManager(
    #     bot=bot,
    #     bot_schema=bot_schema,
    #     data_builder=data_builder,
    # )
    # bot_button_manager.register_buttons(buttons_to_register)
    # if send_executor is not None:
    #     bot_button_manager.with_send_executor(send_executor)
    #
    # register_switch_state_handlers(dp, bot_button_manager)
    # dp.workflow_data.update(
    #     {
    #         MANAGER_KEY: bot_button_manager,
    #     }
    # )

    dialog_schematic = get_dialog_schematic(dp)
    dialog_schematic_manager = DialogSchematicManager(dialog_schematic)
    dp.workflow_data.update(
        {
            MANAGER_KEY: dialog_schematic_manager,
        }
    )

    return dialog_schematic_manager
