from dishka import provide, from_context, Scope
from dishka.provider import Provider
from pika import PlainCredentials, ConnectionParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from goToVladi.core.config.models import MQConfig
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class SyncMQProvider(Provider):
    scope = Scope.APP
    config = from_context(FlaskAppConfig)

    @provide
    def get_credentials(self, config: MQConfig) -> PlainCredentials:
        return PlainCredentials(
            username=config.user,
            password=config.password,
        )

    @provide
    def get_connection(
            self, credentials: PlainCredentials, config: MQConfig
    ) -> BlockingConnection:
        return BlockingConnection(
            ConnectionParameters(
                host=config.host,
                port=config.port,
                credentials=credentials,
            )
        )

    @provide
    def get_channel(self, connection: BlockingConnection) -> BlockingChannel:
        return connection.channel()
