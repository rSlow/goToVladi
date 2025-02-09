from datetime import datetime

from pydantic import ConfigDict


class ORMMixin:
    model_config = ConfigDict(from_attributes=True)


class SocialMixin:
    vk: str | None = None
    instagram: str | None = None
    whatsapp: str | None = None
    telegram: str | None = None


class TimeMixin:
    created_at: datetime | None = None
    edited_at: datetime | None = None
