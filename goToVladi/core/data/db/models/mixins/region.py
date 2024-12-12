from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship, declared_attr


class RegionMixin:
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="SET NULL"), nullable=True
    )

    @declared_attr
    def region(self):
        return relationship("Region", foreign_keys=self.region_id, uselist=False)
