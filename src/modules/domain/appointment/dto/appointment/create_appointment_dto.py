from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAppointmentDto(BaseModel):
    date: date
    user_id: UUID = Field(alias="user")

    class Config:
        orm_mode = True
