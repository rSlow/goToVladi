from dishka import Scope, provide, Provider

from goToVladi.core.data.db.dao import DaoHolder


class DaoProvider(Provider):
    dao = provide(DaoHolder, scope=Scope.REQUEST)
