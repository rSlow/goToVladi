from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class DeliveryMedia(AttachmentProtocol[dto.DeliveryMedia], Base):
    __tablename__ = "delivery_medias"

    delivery_id: Mapped[int] = mapped_column(
        ForeignKey('deliveries.id', ondelete="CASCADE"),
    )
    delivery = relationship("Delivery", back_populates="medias", uselist=False)
