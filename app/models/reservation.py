from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_models import Base


class ReservationORM(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)

    # Внешний ключ с каскадным удалением и NOT NULL
    table_id: Mapped[int] = mapped_column(
        ForeignKey("tables.id", ondelete="CASCADE"), nullable=False
    )

    # Обязательно указываем timezone=True
    reservation_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    duration_minutes: Mapped[int] = mapped_column(nullable=False)

    table: Mapped["TableORM"] = relationship(back_populates="reservations")
