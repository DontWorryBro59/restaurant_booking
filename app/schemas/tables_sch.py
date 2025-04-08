from pydantic import BaseModel
from typing import Optional

class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None

class TableCreate(TableBase):
    pass

class TableRead(TableBase):
    id: int

    model_config = {
        "from_attributes": True
    }