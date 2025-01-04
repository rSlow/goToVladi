from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class MassageMedia(AttachmentProtocol, Base):
    __tablename__ = "massage_medias"

    massage_id: Mapped[int] = mapped_column(ForeignKey('massages.id', ondelete="CASCADE"))
    massage = relationship("Massage", back_populates="medias", uselist=False)

    def to_dto(self) -> dto.MassageMedia:
        return dto.MassageMedia(
            id_=self.id,
            content=self.convert_content(),
            massage_id=self.massage_id
        )
