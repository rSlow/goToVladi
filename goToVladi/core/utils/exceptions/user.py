from .base import BaseError


class NoUsernameFound(BaseError):
    notify_user = "По этому username ничего не найдено"

    def __init__(self, username: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.username = username
