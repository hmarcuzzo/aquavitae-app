from pydantic import constr

from src.core.common.dto.base_dto import BaseDto


class AppointmentGoalDto(BaseDto):
    description: constr(max_length=1000)

    class Config:
        orm_mode = True
