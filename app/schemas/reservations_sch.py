from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.core.custom_logger import get_logger

logger = get_logger(__name__)


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=3, max_length=255)
    table_id: int = Field(..., gt=0)
    reservation_time: datetime
    duration_minutes: int = Field(..., ge=15, le=300)

    @field_validator("reservation_time")
    def validate_reservation_time(cls, value: datetime) -> datetime:
        # Проверка наличия информации о временной зоне
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            message = "Время бронирования должно содержать информацию о временной зоне."
            logger.error(message)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        # Получение текущего времени в UTC
        current_time = datetime.now(timezone.utc)

        # Проверка, что время бронирования в будущем
        if value <= current_time:
            message = "Время бронирования должно быть в будущем."
            logger.error(message)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        return value


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReservationUpdate(BaseModel):
    customer_name: Optional[str] = None
    table_id: Optional[int] = None
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
