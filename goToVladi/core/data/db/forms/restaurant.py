from dataclasses import dataclass

from fastapi import UploadFile, File, Form
from pydantic import AnyHttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumber


@dataclass
class RestaurantInputForm:
    name: str = Form()
    average_check: int = Form()
    rating: float = Form()
    cuisine_id: int = Form()

    photos: list[UploadFile] = File(default_factory=list)

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
