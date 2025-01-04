from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumberType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.massage.media import MassageMedia
from goToVladi.core.data.db.models.mixins import RegionMixin


class Massage(RegionMixin, Base):
    __tablename__ = "massages"

    name: Mapped[str]
    rating: Mapped[float | None]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    min_price: Mapped[int | None]
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias: Mapped[list[MassageMedia]] = relationship(cascade="all, delete-orphan")

    def to_dto(self):
        return dto.Massage(
            id_=self.id,
            name=self.name,
            description=self.description,
            min_price=self.min_price,
            phone=self.phone,
            medias=[_media.to_dto() for _media in self.medias],
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )

    def to_list_dto(self):
        return dto.ListMassage(
            id_=self.id,
            name=self.name,
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )
