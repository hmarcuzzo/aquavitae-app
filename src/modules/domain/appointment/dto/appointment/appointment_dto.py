from datetime import date
from typing import Union
from uuid import UUID

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.appointment_status import AppointmentStatus
from src.modules.infrastructure.user.dto.user_dto import UserDto


class AppointmentDto(BaseDto):
    date: date
    status: AppointmentStatus
    user: Union[UserDto, UUID]

    def __init__(self, **kwargs):
        if "user" not in kwargs:
            kwargs["user"] = kwargs["user_id"]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
