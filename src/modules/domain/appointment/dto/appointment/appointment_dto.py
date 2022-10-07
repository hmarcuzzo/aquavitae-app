from datetime import date
from typing import List, Union
from uuid import UUID

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.appointment_status import AppointmentStatus
from src.modules.domain.appointment.dto.appointment_goal.appointment_goal_dto import (
    AppointmentGoalDto,
)
from src.modules.infrastructure.user.dto.user_dto import UserDto


class AppointmentDto(BaseDto):
    date: date
    status: AppointmentStatus
    user: Union[UserDto, UUID]
    appointment_goals: Union[List[AppointmentGoalDto], List[UUID]] = []

    def __init__(self, **kwargs):
        kwargs["appointment_goals"] = (
            [] if "appointment_goals" not in kwargs else kwargs["appointment_goals"]
        )

        if "user" not in kwargs:
            kwargs["user"] = kwargs["user_id"]
        if "appointment_has_goals" in kwargs:
            for goal in kwargs["appointment_has_goals"]:
                if goal.appointment_goal:
                    kwargs["appointment_goals"] += [goal.appointment_goal]
                else:
                    kwargs["appointment_goals"] += [goal.appointment_goal_id]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
        validate_assignment = True
