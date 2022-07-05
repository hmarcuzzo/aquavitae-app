from datetime import date, time
from typing import Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.personal_data.dto.activity_level.activity_level_dto import ActivityLevelDto
from src.modules.infrastructure.user.dto.user_dto import UserDto


class PersonalDataDto(BaseDto):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    birthday: date
    occupation: constr(max_length=255)
    food_history: Optional[constr(max_length=1000)]
    bedtime: time
    wake_up: time
    activity_level: Union[ActivityLevelDto, UUID]
    user: Union[UserDto, UUID]

    def __init__(self, **kwargs):
        if "activity_level" not in kwargs:
            kwargs["activity_level"] = kwargs["activity_level_id"]
        if "user" not in kwargs:
            kwargs["user"] = kwargs["user_id"]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
