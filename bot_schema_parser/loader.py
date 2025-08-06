from abc import abstractmethod, ABC
from typing import Any, Callable, TypeVar, Protocol, Hashable

from sqlalchemy import JSON, insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from .buttons.base import ApiButton
from .message import ApiMessage

MP = TypeVar("MP")


class DataFormer(Protocol):
    @abstractmethod
    async def form_data(self) -> Any: ...

    @abstractmethod
    async def parse_data(self) -> Any: ...


class ButtonConfigLoader(ABC):
    def __init__(self, message_identifier_parser: Callable[[str], MP] = int):
        self._message_identifier_parser = message_identifier_parser

    def parse_message(self, message_identifier: str) -> MP:
        return self._message_identifier_parser(message_identifier)

    @abstractmethod
    async def load_button_config(self, button_config_identifier: Hashable) -> ApiMessage | None: ...

    @abstractmethod
    async def save_button_config(self, button: ApiButton) -> Hashable: ...


class PostgresqlMessageConfig:
    """
    Create your database class:

        class MyPostgresqlMessageConfig(Base, PostgresqlMessageConfig):
            pass

    """

    __tablename__ = "message_config"

    id: Mapped[int] = mapped_column(primary_key=True)
    button_data: dict = mapped_column(JSON)


class PostgresqlButtonConfigLoader(ButtonConfigLoader):
    def __init__(
            self,
            message_identifier_parser: Callable[[str], MP],
            database_class: type[PostgresqlMessageConfig],
            session_maker: async_sessionmaker[AsyncSession],
    ):
        super().__init__(message_identifier_parser)

        self._database = database_class
        self._session_maker = session_maker

    async def load_button_config(self, button_config_identifier: int) -> ApiMessage | None:
        async with self._session_maker() as session:
            res = await session.scalars(
                select(self._database)
                .where(self._database.id == button_config_identifier)
            )
            return res.one_or_none()

    async def save_button_config(self, button: ApiButton) -> int:
        async with self._session_maker() as session:
            async with session.begin():
                res = await session.execute(
                    insert(self._database)
                    .values(button_data=button.model_dump(mode="json"))
                    .returning(self._database.id)
                )
                await session.commit()
                await session.flush()

        return res.scalar_one()
