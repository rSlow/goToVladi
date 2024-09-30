from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db.models import Region


class RegionMixin:
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id"), nullable=True
    )
    region: Mapped[Region] = relationship(foreign_keys=region_id)
