from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class BreakfastMedia(AttachmentProtocol[dto.BreakfastMedia], Base):
    __tablename__ = "breakfast_medias"

    breakfast_id: Mapped[int] = mapped_column(ForeignKey("breakfasts.id", ondelete="CASCADE"))
    breakfast = relationship("Breakfast", back_populates="medias", uselist=False)
