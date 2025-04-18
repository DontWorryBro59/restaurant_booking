from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_models import Base


class TableORM(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    seats: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    reservations: Mapped[list["ReservationORM"]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
