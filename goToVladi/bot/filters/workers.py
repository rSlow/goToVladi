from goToVladi.core.data.db import dto


async def superusers_worker(*_, user: dto.User, **__):
    return user.is_superuser
