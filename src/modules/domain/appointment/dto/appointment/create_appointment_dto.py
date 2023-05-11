from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAppointmentDto(BaseModel):
    date: datetime
    user_id: UUID = Field(alias="user")
    nutritionist_id: UUID = Field(alias="nutritionist")
    goals: Optional[List[UUID]]

    class Config:
        orm_mode = True
