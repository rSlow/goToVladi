from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db.models import Base


class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
