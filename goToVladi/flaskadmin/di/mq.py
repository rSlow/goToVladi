from dishka import provide, from_context, Scope
from dishka.provider import Provider
from pika import PlainCredentials, ConnectionParameters, BlockingConnection

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class SyncMQProvider(Provider):
    scope = Scope.APP
    config = from_context(FlaskAppConfig)

    @provide
    def get_credentials(self, config: FlaskAppConfig) -> PlainCredentials:
        return PlainCredentials(
            username=config.mq.user,
            password=config.mq.password,
        )

    @provide
    def get_connection(
            self, credentials: PlainCredentials, config: FlaskAppConfig
    ) -> BlockingConnection:
        return BlockingConnection(
            ConnectionParameters(
                host=config.mq.host,
                port=config.mq.port,
                credentials=credentials,
            )
        )
