from typing import Iterable

from dishka import Provider, Scope, provide
from sqlalchemy import Engine as SyncEngine
from sqlalchemy.orm import (
    Session as SyncSession,
    sessionmaker as sync_sessionmaker
)

from goToVladi.core.config.models.db import DBConfig
from goToVladi.core.factory import db


class SyncDbProvider(Provider):
    scope = Scope.APP

    @provide
    def get_engine(self, db_config: DBConfig) -> Iterable[SyncEngine]:
        engine = db.sync.create_engine(db_config)
        yield engine
        engine.dispose(True)

    @provide
    def get_pool(self, engine: SyncEngine) -> sync_sessionmaker[SyncSession]:
        return db.sync.create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    def get_session(
            self, pool: sync_sessionmaker[SyncSession]
    ) -> Iterable[SyncSession]:
        with pool() as session:
            yield session
