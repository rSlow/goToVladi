from aiogram_dialog import Dialog, Window

from goToVladi.bot.apps.admin.states import MailingSG

mailing_dialog = Dialog(
    Window(
        state=MailingSG.text
    ),
    Window(
        state=MailingSG.approve
    ),
)
