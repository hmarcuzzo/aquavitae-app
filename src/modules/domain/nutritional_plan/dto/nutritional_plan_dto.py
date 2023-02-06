from typing import Optional, Union
from uuid import UUID

from pydantic import conint

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.periods import Periods
from src.modules.infrastructure.user.dto.user_dto import UserDto


class NutritionalPlanDto(BaseDto):
    calories_limit: Optional[conint()]
    lipids_limit: Optional[conint()]
    proteins_limit: Optional[conint()]
    carbohydrates_limit: Optional[conint()]
    period_limit: Optional[Periods]
    active: Optional[bool]
    user: Optional[Union[UserDto, UUID]]

    def __init__(self, **kwargs):
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
