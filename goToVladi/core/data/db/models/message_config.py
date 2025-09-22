from dialog_schematic_manager.loader import PostgresqlMessageConfig
from goToVladi.core.data.db.models import Base


class MessageConfig(Base, PostgresqlMessageConfig):
    pass
