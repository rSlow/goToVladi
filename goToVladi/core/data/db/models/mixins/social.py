from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_utils import URLType


class SocialMixin:
    vk: Mapped[str | None] = mapped_column(URLType, nullable=True)
    instagram: Mapped[str | None] = mapped_column(URLType, nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(URLType, nullable=True)
    telegram: Mapped[str | None] = mapped_column(URLType, nullable=True)
