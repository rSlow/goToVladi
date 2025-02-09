from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base

CarRentsClasses = Table(
    "car_rents_classes",
    Base.metadata,
    Column(
        "car_rent_id",
        ForeignKey("car_rents.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "car_class_id",
        ForeignKey("car_classes.id", ondelete="CASCADE"),
        primary_key=True
    ),
)


class CarClass(Base):
    __tablename__ = "car_classes"

    name: Mapped[str]
    description: Mapped[str | None]
    car_rents = relationship(
        "CarRent", secondary=CarRentsClasses, back_populates="car_classes", uselist=True
    )

    def to_dto(self):
        return dto.CarClass.model_validate(self)

    def __repr__(self):
        return self.name
