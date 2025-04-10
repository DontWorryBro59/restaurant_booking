from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TableBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    seats: int = Field(..., ge=1, le=10)
    location: Optional[str] = Field(None, min_length=3, max_length=255)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Table 1", "seats": 4, "location": "Near the window"}
        }
    )


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Table 1",
                "seats": 4,
                "location": "Near the window",
            }
        },
    )


class TableUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    seats: Optional[int] = Field(None, ge=1, le=10)
    location: Optional[str] = Field(None, min_length=3, max_length=255)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Table 2", "seats": 2, "location": "By the door"}
        }
    )
