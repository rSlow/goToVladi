from abc import ABC

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection


class BaseInjectContext(ABC):
    # @bomzheg, it's laugh)
    """
    ATTENTION!
    GLOBAL VARIABLE!
    """

    container: AsyncContainer | None = None

    @classmethod
    def inject(cls, func):
        async def wrapper(*args, **kwargs):
            if cls.container is None:
                raise RuntimeError(
                    "Inject context container has not been initialized"
                )

            async with cls.container() as request_container:
                wrapped = wrap_injection(
                    func=func,
                    remove_depends=True,
                    container_getter=lambda _, __: request_container,
                    is_async=True,
                )
                return await wrapped(*args, **kwargs)

        return wrapper
