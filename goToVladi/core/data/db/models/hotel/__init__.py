from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from .district import HotelDistrict
from .media import HotelMedia


class Hotel(Base):
    __tablename__ = "hotels"

    name: Mapped[str]
    site_url: Mapped[str | None] = mapped_column(URLType, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("hotel_districts.id", ondelete="SET NULL"), nullable=True
    )
    district: Mapped[HotelDistrict] = relationship(
        foreign_keys=district_id, back_populates="hotels"
    )

    medias: Mapped[list[HotelMedia]] = relationship(cascade="all, delete-orphan")
    min_price: Mapped[int]
    promo_code: Mapped[str | None]

    def to_list_dto(self) -> dto.ListHotel:
        return dto.ListHotel(
            id_=self.id,
            name=self.name,
            district=self.district.to_dto(),
            min_price=self.min_price
        )

    def to_dto(self) -> dto.Hotel:
        return dto.Hotel(
            id_=self.id,
            name=self.name,
            district=self.district.to_dto() if self.district else None,
            district_id=self.district_id,
            site_url=self.site_url,
            description=self.description,
            medias=[_media.to_dto() for _media in self.medias],
            min_price=self.min_price,
            promo_code=self.promo_code,
        )
