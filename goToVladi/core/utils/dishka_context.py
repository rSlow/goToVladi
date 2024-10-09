from abc import ABC

from dishka import AsyncContainer, Container
from dishka.integrations.base import wrap_injection


class BaseInjectContext(ABC):
    # @bomzheg, it's laugh)
    """
    ATTENTION!
    GLOBAL VARIABLE!
    """

    container: Container | AsyncContainer | None = None

    @classmethod
    def _check_container(cls, is_async: bool) -> None:
        if cls.container is None:
            raise RuntimeError(
                "Inject context container has not been initialized"
            )
        if isinstance(cls.container, Container) and is_async:
            raise AttributeError(
                "For `@inject` decorator you have to use AsyncContainer. "
                "Use `@sync_inject` decorator instead."
            )
        elif isinstance(cls.container, AsyncContainer) and not is_async:
            raise AttributeError(
                "For `@sync_inject` decorator you have to use Container (sync)."
                " Use `@inject` decorator instead."
            )
        else:
            raise TypeError(
                f"{cls.container} is {cls.container.__class__.__name__}, "
                "not Container or AsyncContainer"
            )

    @classmethod
    def inject(cls, func):
        cls._check_container(is_async=True)

        async def wrapper(*args, **kwargs):
            async with cls.container() as request_container:
                wrapped = wrap_injection(
                    func=func,
                    remove_depends=True,
                    container_getter=lambda _, __: request_container,
                    is_async=True,
                )
                return await wrapped(*args, **kwargs)

        return wrapper

    @classmethod
    def sync_inject(cls, func):
        cls._check_container(is_async=False)

        def wrapper(*args, **kwargs):
            with cls.container() as request_container:
                wrapped = wrap_injection(
                    func=func,
                    remove_depends=True,
                    container_getter=lambda _, __: request_container,
                    is_async=False,
                )
                return wrapped(*args, **kwargs)

        return wrapper
