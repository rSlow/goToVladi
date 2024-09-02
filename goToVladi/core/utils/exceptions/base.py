from abc import ABC

from goToVladi.core.data.db import dto


class BaseError(Exception, ABC):
    notify_user = "Ошибка"

    def __init__(
            self,
            text: str = "",
            user_id: int | None = None,
            user: dto.User | None = None,
            alarm: bool | None = False,
            notify_user: str | None = None,
            *args,
            **kwargs,
    ) -> None:
        super().__init__(args, kwargs)
        self.text = text
        self.user_id = user_id
        self.user = user
        self.alarm = alarm
        self.notify_user = notify_user or self.notify_user

    def __repr__(self) -> str:
        result_msg = f"Error: {self.text}"
        if self.user_id:
            result_msg += f", by user {self.user_id}"
        if self.notify_user:
            result_msg += f". Information for user: {self.notify_user}"
        return result_msg

    def __str__(self) -> str:
        return (
            f"Error.\ntype: {self.__class__.__name__}\n"
            f"text: {self.text}\n"
            f"notify info: {self.notify_user}"
        )
