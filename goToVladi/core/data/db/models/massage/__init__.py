from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import PhoneNumberType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.massage.media import MassageMedia
from goToVladi.core.data.db.models.mixins import RegionMixin, BaseCardMixin
from goToVladi.core.data.db.utils.media import get_medias_field


class Massage(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "massages"

    rating: Mapped[float | None]
    min_price: Mapped[int | None]
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias = get_medias_field(MassageMedia)

    def to_dto(self):
        return dto.Massage(
            id=self.id,
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
            id=self.id,
            name=self.name,
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )
