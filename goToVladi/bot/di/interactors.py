from dishka import Provider, Scope, provide_all

from goToVladi.bot.utils.interactors.error_mesasage import ErrorMessageInteractor


class InteractorProvider(Provider):
    scope = Scope.APP

    interactors = provide_all(
        ErrorMessageInteractor,
    )
