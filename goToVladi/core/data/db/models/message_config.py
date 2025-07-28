from bot_schema_parser.loader import PostgresqlMessageConfig
from goToVladi.core.data.db.models import Base


class MessageConfig(Base, PostgresqlMessageConfig):
    pass
