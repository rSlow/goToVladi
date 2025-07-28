from goToVladi.bot.views.alert import BotAlert


class ErrorMessageInteractor:
    def __init__(self, alert: BotAlert):
        self.alert = alert

    async def __call__(self, exc: Exception):
        if exc.args:
            await self.alert(exc.args[0])
