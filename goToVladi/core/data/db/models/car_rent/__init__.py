from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import PhoneNumberType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin
from .car_class import CarRentsClasses, CarClass
from .media import CarRentMedia


class CarRent(RegionMixin, Base):
    __tablename__ = "car_rents"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[float | None]
    min_age: Mapped[int | None]
    min_experience: Mapped[int | None]
    min_price: Mapped[int | None]
    phone: Mapped[str | None] = mapped_column(PhoneNumberType(region="RU"), nullable=True)

    car_classes: Mapped[list[CarClass]] = relationship(
        secondary=CarRentsClasses, back_populates="car_rents",
    )
    medias: Mapped[list[CarRentMedia]] = relationship(cascade="all, delete-orphan")

    def to_list_dto(self) -> dto.ListCarRent:
        return dto.ListCarRent(
            id_=self.id,
            name=self.name,
        )

    def to_dto(self) -> dto.CarRent:
        return dto.CarRent(
            id_=self.id,
            name=self.name,
            description=self.description,
            rating=self.rating,
            min_age=self.min_age,
            min_experience=self.min_experience,
            min_price=self.min_price,
            phone=self.phone,
            car_classes=[_car_class.to_dto() for _car_class in self.car_classes],
            medias=[_media.to_dto() for _media in self.medias],
        )
