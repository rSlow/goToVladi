from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class SeaRecreationMedia(AttachmentProtocol[dto.SeaRecreationMedia], Base):
    __tablename__ = "sea_recreation_medias"

    sea_recreation_id: Mapped[int] = mapped_column(
        ForeignKey("sea_recreations.id", ondelete="CASCADE")
    )
    sea_recreation = relationship("SeaRecreation", back_populates="medias", uselist=False)
