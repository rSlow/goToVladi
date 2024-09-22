from typing import Callable

from aiogram import types


def is_superuser(superusers: list[int]) -> Callable:
    async def _is_superuser(message: types.Message) -> bool:
        user = message.from_user
        if not isinstance(user, types.User):
            raise TypeError(
                f"user {str(user)} is {type(user)}, not 'types.User' type"
            )
        return user.id in superusers

    return _is_superuser
