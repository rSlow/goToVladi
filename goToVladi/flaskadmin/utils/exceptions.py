from abc import ABC


class FormError(Exception, ABC):
    message: str = "Ошибка формы."


class AccessDeniedError(FormError):
    message = "Доступ запрещен."


class InvalidCredentialsError(AccessDeniedError):
    message = "Неверные учётные данные."


class OutdatedCredentialsError(AccessDeniedError):
    message = "Устаревшие данные авторизации. Попробуйте войти еще раз."
