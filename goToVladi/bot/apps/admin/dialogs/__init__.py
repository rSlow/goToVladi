from aiogram import Router

from goToVladi.bot.apps.admin.dialogs.main import setup_admin_apps


def setup():
    router = Router(name=__name__)

    router.include_router(setup_admin_apps())

    return router
