from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAppointmentDto(BaseModel):
    date: date
    user_id: UUID = Field(alias="user")
    goals: Optional[List[UUID]]

    class Config:
        orm_mode = True
