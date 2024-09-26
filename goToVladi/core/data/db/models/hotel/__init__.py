from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from .media import HotelMedia


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    district: Mapped[str]
    site_url = mapped_column(URLType, nullable=True)
    description = mapped_column(Text, nullable=True)

    medias: Mapped[list[HotelMedia]] = relationship()
    min_price: Mapped[int]
    promo_code: Mapped[str] = mapped_column(nullable=True)

    def to_list_dto(self) -> dto.ListHotel:
        return dto.ListHotel(
            id_=self.id,
            name=self.name,
            district=self.district,
            min_price=self.min_price
        )

    def to_dto(self) -> dto.Hotel:
        return dto.Hotel(
            id_=self.id,
            name=self.name,
            district=self.district,
            site_url=self.site_url,
            description=self.description,
            medias=[
                _media.to_dto()
                for _media in self.medias
            ],
            min_price=self.min_price,
            promo_code=self.promo_code,
        )
