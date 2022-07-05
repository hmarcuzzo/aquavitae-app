from datetime import date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class CreatePersonalDataDto(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    birthday: date
    occupation: constr(max_length=255)
    food_history: Optional[constr(max_length=1000)]
    bedtime: time
    wake_up: time
    activity_level_id: UUID = Field(alias="activity_level")
    user_id: UUID = Field(alias="user")

    class Config:
        extra = Extra.forbid
