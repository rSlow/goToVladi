from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType, PhoneNumberType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.food.cuisine import FoodCuisine
from goToVladi.core.data.db.models.mixins import RegionMixin, BaseCardMixin, SocialMixin
from goToVladi.core.data.db.utils.media import get_medias_field
from .media import DeliveryMedia


class Delivery(BaseCardMixin, RegionMixin, SocialMixin, Base):
    __tablename__ = "deliveries"

    average_check: Mapped[int]
    site_url: Mapped[str | None] = mapped_column(URLType, nullable=True)
    rating: Mapped[float]
    priority: Mapped[float] = mapped_column(default=0)
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias = get_medias_field(DeliveryMedia)

    cuisine_id: Mapped[int | None] = mapped_column(
        ForeignKey("restaurant_cuisines.id"), nullable=True
    )
    cuisine: Mapped[FoodCuisine] = relationship(foreign_keys=cuisine_id)

    def to_list_dto(self) -> dto.ListDelivery:
        return dto.ListDelivery.model_validate(self)

    def to_dto(self) -> dto.Delivery:
        return dto.Delivery.model_validate(self)
