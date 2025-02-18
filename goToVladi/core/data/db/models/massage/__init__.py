from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.massage.media import MassageMedia
from goToVladi.core.data.db.models.mixins import RegionMixin, BaseCardMixin
from goToVladi.core.data.db.types.phone import PhoneNumberType
from goToVladi.core.data.db.utils.media import get_medias_field


class Massage(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "massages"

    rating: Mapped[float | None]
    min_price: Mapped[int | None]
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias = get_medias_field(MassageMedia)

    def to_list_dto(self) -> dto.ListMassage:
        return dto.ListMassage.model_validate(self)

    def to_dto(self) -> dto.Massage:
        return dto.Massage.model_validate(self)
