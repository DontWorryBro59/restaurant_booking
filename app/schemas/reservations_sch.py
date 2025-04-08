from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=3, max_length=255)
    table_id: int = Field(..., gt=0)
    reservation_time: datetime
    duration_minutes: int = Field(..., ge=15, le=300)

    @field_validator("reservation_time")
    def validate_reservation_time(cls, value):
        if value < datetime.now():
            raise ValueError("Reservation time must be in the future.")
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