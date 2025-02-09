from typing import TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from goToVladi.core.data.db.dto.attachment import AttachmentType
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


def create_media_class(
        classname: str, tablename: str, parent_id_prop_name: str, parent_class_name: str,
        parent_id_field_name: str, parent_obj_field_name: str, dto_class: AttachmentType,
) -> type[AttachmentProtocol]:
    def to_dto(self) -> dto_class:
        return dto_class(
            id_=self.id,
            content=self.convert_content(),
            restaurant_id=self.restaurant_id
        )

    _cls = type(
        classname,
        (AttachmentProtocol, Base),
        {
            "__tablename__": tablename,
            parent_id_field_name: mapped_column(
                ForeignKey(parent_id_prop_name, ondelete="CASCADE")
            ),
            parent_obj_field_name: relationship(
                parent_class_name, back_populates="medias", uselist=False
            ),
            "to_dto": to_dto,
        }
    )
    return _cls  # noqa


Attachment = TypeVar("Attachment", bound=AttachmentProtocol)


def get_medias_field(_class: type[Attachment]) -> Mapped[list[Attachment]]:
    return relationship(_class, cascade="all, delete-orphan", uselist=True)
