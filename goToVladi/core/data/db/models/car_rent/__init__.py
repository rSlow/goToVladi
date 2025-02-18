from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin, BaseCardMixin
from goToVladi.core.data.db.types.phone import PhoneNumberType
from goToVladi.core.data.db.utils.media import get_medias_field
from .car_class import CarRentsClasses, CarClass
from .media import CarRentMedia


class CarRent(BaseCardMixin, RegionMixin, Base):
    __tablename__ = "car_rents"

    rating: Mapped[float | None]
    min_age: Mapped[int | None]
    min_experience: Mapped[int | None]
    min_price: Mapped[int | None]
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)
    site_url: Mapped[str | None] = mapped_column(URLType, nullable=True)
    car_classes: Mapped[list[CarClass]] = relationship(
        secondary=CarRentsClasses, back_populates="car_rents",
    )
    medias = get_medias_field(CarRentMedia)

    def to_list_dto(self) -> dto.ListCarRent:
        return dto.ListCarRent.model_validate(self)

    def to_dto(self) -> dto.CarRent:
        return dto.CarRent.model_validate(self)
