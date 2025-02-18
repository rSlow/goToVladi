from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.food.bar.media import BarMedia
from goToVladi.core.data.db.models.mixins import RegionMixin
from goToVladi.core.data.db.models.mixins.base_card import BaseCardMixin
from goToVladi.core.data.db.types.phone import PhoneNumberType
from goToVladi.core.data.db.utils.media import get_medias_field


class Bar(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "bars"

    average_check: Mapped[int | None] = None
    rating: Mapped[float | None] = None
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias = get_medias_field(BarMedia)

    def to_list_dto(self):
        return dto.ListBar.model_validate(self)

    def to_dto(self):
        return dto.Bar.model_validate(self)
