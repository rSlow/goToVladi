from faststream.broker.core.usecase import BrokerUsecase
from faststream.rabbit import RabbitBroker

from goToVladi.mq.config.models import MQAppConfig


def create_broker(config: MQAppConfig) -> BrokerUsecase:
    return RabbitBroker(
        url=config.mq.uri,
        max_consumers=10
    )
