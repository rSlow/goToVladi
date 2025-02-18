from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin
from goToVladi.core.data.db.models.mixins.base_card import BaseCardMixin
from goToVladi.core.data.db.types.phone import PhoneNumberType
from goToVladi.core.data.db.utils.media import get_medias_field
from .media import BreakfastMedia


class Breakfast(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "breakfasts"

    average_check: Mapped[int | None] = None
    rating: Mapped[float | None] = None
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    medias = get_medias_field(BreakfastMedia)

    def to_list_dto(self):
        return dto.ListBreakfast.model_validate(self)

    def to_dto(self):
        return dto.Breakfast.model_validate(self)
