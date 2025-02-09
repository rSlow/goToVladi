from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class BarMedia(AttachmentProtocol[dto.BarMedia], Base):
    __tablename__ = "bar_medias"

    bar_id: Mapped[int] = mapped_column(ForeignKey("bars.id", ondelete="CASCADE"))
    bar = relationship("Bar", back_populates="medias", uselist=False)

