from abc import ABC


class BaseError(Exception, ABC):
    message = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.message, *args, **kwargs)
    # def __init__(
    #         self,
    #         text: str = "",
    #         user_id: int | None = None,
    #         chat_id: int | None = None,
    #         user: dto.User | None = None,
    #         alarm: bool | None = False,
    #         notify_user: str | None = None,
    #         *args,
    #         **kwargs,
    # ) -> None:
    #     super().__init__(args, kwargs)
    #     self.text = text
    #     self.user_id = user_id
    #     self.chat_id = chat_id
    #     self.user = user
    #     self.alarm = alarm
    #     self.message = notify_user or self.message
    #
    # def __repr__(self) -> str:
    #     result_msg = f"Error: {self.text}"
    #     if self.user_id:
    #         result_msg += f", by user {self.user_id}"
    #     if self.chat_id:
    #         result_msg += f", in chat {self.chat_id}"
    #     if self.message:
    #         result_msg += f". Information for user: {self.message}"
    #     return result_msg
    #
    # def __str__(self) -> str:
    #     return (
    #         f"Error.\ntype: {self.__class__.__name__}\n"
    #         f"text: {self.text}\n"
    #         f"notify info: {self.message}"
    #     )
