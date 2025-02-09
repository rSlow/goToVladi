from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin, BaseCardMixin
from goToVladi.core.data.db.types.url import PydanticURLType
from goToVladi.core.data.db.utils.media import get_medias_field
from .media import TripMedia


class Trip(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "trips"

    site_url: Mapped[str | None] = mapped_column(PydanticURLType, nullable=True)
    medias = get_medias_field(TripMedia)

    def to_list_dto(self):
        return dto.ListTrip.model_validate(self)

    def to_dto(self):
        return dto.Trip.model_validate(self)

    def __str__(self):
        res = ""
        if self.region:
            res += f"{self.region.name}: "
        return res + self.name
