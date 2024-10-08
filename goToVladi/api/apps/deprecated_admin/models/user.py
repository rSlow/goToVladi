from dishka import FromDishka
from fastadmin import SqlAlchemyModelAdmin

from goToVladi.api.apps.admin.ulits.inject_context import AdminInjectContext
from goToVladi.api.utils.auth import AuthService
from goToVladi.core.data.db.dao import DaoHolder


class UserAdmin(SqlAlchemyModelAdmin):
    list_display = ("username", "first_name", "last_name",)
    list_display_links = ("username",)
    list_filter = ("username", "is_superuser")
    search_fields = ("username",)
    exclude = ("hashed_password",)

    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

    @AdminInjectContext.inject
    async def authenticate(
            self, username: str, password: str,
            auth_service: FromDishka[AuthService], dao: FromDishka[DaoHolder]
    ):
        user = await auth_service.authenticate_user(username, password, dao)
        if user.is_superuser and user.id_ is not None:
            return user.id_
        return None

    @AdminInjectContext.inject
    async def change_password(
            self, id_: int, password: str,
            auth_service: FromDishka[AuthService], dao: FromDishka[DaoHolder],
    ) -> None:
        user = await dao.user.get_by_id(id_)
        await auth_service.update_user_password(user, password, dao)
