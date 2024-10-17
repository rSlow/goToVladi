from abc import ABC

from goToVladi.core.utils.exceptions import BaseError


class FlaskError(BaseError):
    log_message = "Ошибка Flask: {message}"


class FormError(Exception, ABC):
    message: str = "Ошибка формы."


class AccessDeniedError(FormError):
    message = "Доступ запрещен."


class InvalidCredentialsError(AccessDeniedError):
    message = "Неверные учётные данные."


class OutdatedCredentialsError(AccessDeniedError):
    message = "Устаревшие данные авторизации. Попробуйте войти еще раз."
