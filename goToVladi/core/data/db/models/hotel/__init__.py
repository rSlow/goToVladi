from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.utils.media import get_medias_field
from .district import HotelDistrict
from .media import HotelMedia
from ..mixins import BaseCardMixin


class Hotel(BaseCardMixin, Base):
    __tablename__ = "hotels"

    site_url: Mapped[str | None] = mapped_column(URLType, nullable=True)

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("hotel_districts.id", ondelete="SET NULL"), nullable=True
    )
    district: Mapped[HotelDistrict] = relationship(
        foreign_keys=district_id, back_populates="hotels"
    )

    medias = get_medias_field(HotelMedia)
    min_price: Mapped[int]
    promo_code: Mapped[str | None]

    def to_list_dto(self) -> dto.ListHotel:
        return dto.ListHotel.model_validate(self)

    def to_dto(self) -> dto.Hotel:
        return dto.Hotel.model_validate(self)
