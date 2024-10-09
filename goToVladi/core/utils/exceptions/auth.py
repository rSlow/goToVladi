class AuthError(Exception):
    pass


class InvalidCredentialsError(AuthError):
    def __init__(self):
        super().__init__("Неверные учётные данные.")


class UserIsNotSuperuserError(AuthError):
    def __init__(self):
        super().__init__("Доступ запрещен.")
