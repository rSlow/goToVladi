from .base import BaseError


class AuthError(BaseError):
    pass


class AccessDeniedError(AuthError):
    message = "Доступ запрещен."


class InvalidCredentialsError(AccessDeniedError):
    message = "Неверные учётные данные."


class OutdatedCredentialsError(AccessDeniedError):
    message = "Устаревшие данные авторизации. Попробуйте войти еще раз."
