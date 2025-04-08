from typing import Optional

from pydantic import BaseModel, ConfigDict


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TableUpdate(BaseModel):
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
