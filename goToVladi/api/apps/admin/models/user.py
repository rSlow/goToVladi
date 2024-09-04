from dishka import FromDishka
from fastadmin import SqlAlchemyModelAdmin

from goToVladi.api.apps.admin.ulits.inject_context import AdminInjectContext
from goToVladi.api.utils.auth import AuthService
from goToVladi.core.data.db.dao import DaoHolder


class UserAdmin(SqlAlchemyModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    @AdminInjectContext.inject
    async def authenticate(
            self, username: str, password: str,
            auth_service: FromDishka[AuthService], dao: FromDishka[DaoHolder]
    ):
        user = await auth_service.authenticate_user(username, password, dao)
        if user.is_superuser and user.db_id is not None:
            return user.db_id
        return None
