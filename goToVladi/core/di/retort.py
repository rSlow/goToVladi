from adaptix import Retort
from dishka import Provider, Scope, provide

from goToVladi.core.config.parser.retort import get_base_retort


class RetortProvider(Provider):
    scope = Scope.APP

    @provide
    def get_retort(self) -> Retort:
        return get_base_retort()
