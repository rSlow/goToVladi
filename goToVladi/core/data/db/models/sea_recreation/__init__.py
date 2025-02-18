from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin
from goToVladi.core.data.db.models.mixins.base_card import BaseCardMixin
from goToVladi.core.data.db.types.phone import PhoneNumberType
from goToVladi.core.data.db.utils.media import get_medias_field
from .category import SeaRecreationCategory
from .media import SeaRecreationMedia


class SeaRecreation(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "sea_recreations"

    rating: Mapped[float | None] = None
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("sea_recreation_categories.id"), nullable=True
    )
    category: Mapped[SeaRecreationCategory] = relationship(foreign_keys=category_id)

    medias = get_medias_field(SeaRecreationMedia)

    def to_list_dto(self):
        return dto.ListSeaRecreation.model_validate(self)

    def to_dto(self):
        return dto.SeaRecreation.model_validate(self)
