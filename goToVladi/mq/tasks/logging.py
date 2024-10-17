from datetime import datetime

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitExchange

from goToVladi.bot.views.alert import BotAlert

router = RabbitRouter()
log_exchange = RabbitExchange("logging")


@router.subscriber("log", log_exchange)
@inject
async def send_alert(error_text: str, alert: FromDishka[BotAlert]):
    alert_message = {
        "error": error_text,
        "dt": datetime.utcnow().isoformat()
    }
    await alert(text=f"Логирование из очереди: {str(alert_message)}")
