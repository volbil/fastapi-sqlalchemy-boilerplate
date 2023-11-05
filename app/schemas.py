from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from pydantic import model_serializer
from typing import Callable
from pydantic import Field


def convert_datetime_to_timestamp(date: datetime | None) -> int | None:
    date = date.replace(tzinfo=timezone.utc) if date else date
    return int(date.timestamp()) if date else None


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        from_attributes=True,
    )

    def serializable_dict(self, **kwargs):
        default_dict = self.model_dump()
        return jsonable_encoder(default_dict)

    @model_serializer(mode="wrap")
    def serialize(self, original_serializer: Callable) -> dict:
        # Based on https://github.com/pydantic/pydantic/discussions/7199#discussioncomment-6841388

        result = original_serializer(self)

        for field_name, field_info in self.model_fields.items():
            if field_info.annotation == datetime:
                result[field_name] = convert_datetime_to_timestamp(
                    getattr(self, field_name)
                )

        return result


# Responses
class UserResponse(CustomModel):
    username: str | None = Field(examples=["username"])
    created: datetime = Field(examples=[1686088809])
