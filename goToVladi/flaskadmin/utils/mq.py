from dataclasses import dataclass
from typing import Any

from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType


@dataclass
class RabbitQueue:
    name: str
    routing_key: str
    passive: bool = False
    durable: bool = False
    exclusive: bool = False
    auto_delete: bool = False
    arguments: Any | None = None


@dataclass
class RabbitExchange:
    queues: list[RabbitQueue]
    name: str
    type_: ExchangeType = ExchangeType.direct
    passive: bool = False,
    durable: bool = False,
    auto_delete: bool = False,
    internal: bool = False,
    arguments: Any | None = None


def setup(channel: BlockingChannel, exchanges: list[RabbitExchange]):
    for exchange in exchanges:
        channel.exchange_declare(
            exchange=exchange.name, exchange_type=exchange.type_,
            passive=exchange.passive, durable=exchange.durable,
            auto_delete=exchange.auto_delete, internal=exchange.internal,
            arguments=exchange.arguments
        )

        for queue in exchange.queues:
            result = channel.queue_declare(
                queue=queue.name, passive=queue.passive, durable=queue.durable,
                exclusive=queue.exclusive, auto_delete=queue.auto_delete,
                arguments=queue.arguments,
            )
            queue_name = result.method.queue
            channel.queue_bind(
                exchange=exchange.name, queue=queue_name,
                routing_key=queue.routing_key
            )
