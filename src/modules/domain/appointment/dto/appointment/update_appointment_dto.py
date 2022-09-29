from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra, Field

from src.core.constants.enum.appointment_status import AppointmentStatus


class UpdateAppointmentDto(BaseModel):
    date: Optional[date]
    status: Optional[AppointmentStatus]
    user_id: Optional[UUID] = Field(alias="user")

    class Config:
        extra = Extra.forbid
