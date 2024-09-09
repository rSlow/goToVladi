import uuid
from base64 import b64decode

import aiofiles
from dishka import FromDishka
from fastadmin import SqlAlchemyModelAdmin, WidgetType

from goToVladi.api.apps.admin.ulits.inject_context import AdminInjectContext
from goToVladi.core.config import Paths
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.data.db.models import Restaurant


class RestaurantModelAdmin(SqlAlchemyModelAdmin):
    list_display = ("name", "average_check", "rating", "priority")
    list_display_links = ("name",)
    list_filter = ("average_check", "rating", "priority")
    search_fields = ("name",)
    list_select_related = ("cuisine",)
    verbose_name = "Ресторан"
    verbose_name_plural = "Рестораны"
    formfield_overrides = {
        "photo": (WidgetType.Upload, {
            "maxCount": 1,
            "name": "photo"
        }),
        "phone": (WidgetType.PhoneInput, {}),
        "vk": (WidgetType.UrlInput, {}),
        "instagram": (WidgetType.UrlInput, {}),
        "whatsapp": (WidgetType.UrlInput, {}),
        "telegram": (WidgetType.UrlInput, {}),
    }

    @AdminInjectContext.inject
    async def orm_save_upload_field(
            self, obj: Restaurant, field: str, base64: str,
            dao: FromDishka[DaoHolder], paths: FromDishka[Paths]
    ):
        photos_path = paths.upload_file_path / "restaurant_photos" / str(obj.id)
        photos_path.mkdir(parents=True, exist_ok=True)
        filename = uuid.uuid4().hex + ".jpeg"
        async with aiofiles.open(photos_path / filename, "wb") as file:
            base64 = base64.split(",")[1]
            await file.write(b64decode(base64))

        await dao.restaurant.save_restaurant_photo(
            obj.id, photos_path / filename
        )


class RestaurantCuisineModelAdmin(SqlAlchemyModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    verbose_name = "Кухня"
    verbose_name_plural = "Кухни"
