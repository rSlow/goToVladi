from abc import ABC


class BaseError(Exception, ABC):
    message = "Ошибка"

    def __init__(self, **kwargs):
        self.map_args = kwargs

    def __str__(self):
        return self.message.format_map(**self.map_args)
