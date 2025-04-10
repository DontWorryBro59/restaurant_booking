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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_name": "John Doe",
                "table_id": 1,
                "reservation_time": "2025-04-10T18:30:00+00:00",
                "duration_minutes": 90,
            }
        }
    )


class ReservationCreate(ReservationBase):
    pass

    @field_validator("reservation_time")
    def validate_reservation_time(cls, value: datetime) -> datetime:
        # Проверка наличия информации о временной зоне
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            message = "Время бронирования должно содержать информацию о временной зоне."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        # Получение текущего времени в UTC
        current_time = datetime.now(timezone.utc)

        # Проверка, что время бронирования в будущем
        if value <= current_time:
            message = "Время бронирования должно быть в будущем."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        return value


class ReservationRead(ReservationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "table_id": 1,
                "reservation_time": "2025-04-10T18:30:00+00:00",
                "duration_minutes": 90,
            }
        },
    )


class ReservationUpdate(ReservationCreate):
    customer_name: Optional[str] = None
    table_id: Optional[int] = None
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_name": "Jane Doe",
                "table_id": 2,
                "reservation_time": "2025-04-10T19:00:00+00:00",
                "duration_minutes": 60,
            }
        }
    )
