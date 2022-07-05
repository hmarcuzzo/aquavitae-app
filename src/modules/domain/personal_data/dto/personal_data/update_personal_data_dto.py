from datetime import date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class UpdatePersonalDataDto(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    birthday: Optional[date]
    occupation: Optional[constr(max_length=255)]
    food_history: Optional[constr(max_length=1000)]
    bedtime: Optional[time]
    wake_up: Optional[time]
    activity_level_id: Optional[UUID] = Field(alias="activity_level")

    class Config:
        extra = Extra.forbid
