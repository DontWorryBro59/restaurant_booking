from pydantic import BaseModel, ConfigDict


class MessageSchema(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"message": "Your reservation has been confirmed."}
        }
    )
