from dataclasses import dataclass

from fastapi import UploadFile, File, Form
from pydantic import AnyHttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumber

from goToVladi.api.utils.url import url_to_str
from goToVladi.bot.utils.media import as_aiogram_content_type
from goToVladi.core.data.db import models as db


@dataclass
class RestaurantInputForm:
    name: str = Form()
    average_check: int = Form()
    rating: float = Form()
    cuisine_id: int = Form()

    medias: list[UploadFile] = File(default_factory=list)

    is_delivery: bool = Form(default=False)
    is_inner: bool = Form(default=True)

    priority: float | None = Form(default=None)
    site_url: AnyHttpUrl | None = Form(default=None)
    description: str | None = Form(default=None)
    phone: PhoneNumber | None = Form(default=None)

    vk: AnyHttpUrl | None = Form(default=None)
    instagram: AnyHttpUrl | None = Form(default=None)
    whatsapp: AnyHttpUrl | None = Form(default=None)
    telegram: AnyHttpUrl | None = Form(default=None)

    def to_model(self):
        return db.Restaurant(
            name=self.name,
            average_check=self.average_check,
            is_delivery=self.is_delivery,
            is_inner=self.is_inner,
            rating=self.rating,
            cuisine_id=self.cuisine_id,
            medias=[
                db.RestaurantMedia(
                    content_type=as_aiogram_content_type(media.content_type),
                    content=media
                )
                for media in self.medias
            ],
            priority=self.priority,
            site_url=url_to_str(self.site_url),
            description=self.description,
            phone=self.phone,
            vk=url_to_str(self.vk),
            instagram=url_to_str(self.instagram),
            whatsapp=url_to_str(self.whatsapp),
            telegram=url_to_str(self.telegram)
        )
