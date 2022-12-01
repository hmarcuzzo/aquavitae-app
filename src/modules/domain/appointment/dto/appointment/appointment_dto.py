from datetime import date
from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy_utils import InstrumentedList

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.appointment_status import AppointmentStatus
from src.modules.domain.appointment.dto.appointment_goal.appointment_goal_dto import (
    AppointmentGoalDto,
)
from src.modules.domain.appointment.entities.appointment_has_appointment_goal_entity import (
    AppointmentHasAppointmentGoal,
)
from src.modules.infrastructure.user.dto.user_dto import UserDto


class AppointmentDto(BaseDto):
    date: date
    status: AppointmentStatus
    user: Union[UserDto, UUID]
    appointment_has_goals: Optional[Union[List[AppointmentGoalDto], List[UUID]]]

    def __init__(self, **kwargs):
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]

        if "appointment_has_goals" in kwargs and isinstance(
            kwargs["appointment_has_goals"][0], AppointmentHasAppointmentGoal
        ):
            kwargs["appointment_has_goals"] = [
                goal.appointment_goal for goal in kwargs["appointment_has_goals"]
            ]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
        validate_assignment = True
