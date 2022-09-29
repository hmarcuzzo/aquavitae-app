from datetime import date
from typing import Optional, Union
from uuid import UUID

from pydantic import confloat, conint

from src.core.common.dto.base_dto import BaseDto
from src.modules.infrastructure.user.dto.user_dto import UserDto


class AnthropometricDataDto(BaseDto):
    weight: Optional[confloat(ge=0)]
    height: Optional[conint(ge=0)]
    waist_circumference: Optional[conint(ge=0)]
    fat_mass: Optional[confloat(ge=0)]
    muscle_mass: Optional[confloat(ge=0)]
    bone_mass: Optional[confloat(ge=0)]
    body_water: Optional[confloat(ge=0)]
    basal_metabolism: Optional[conint(ge=0)]
    visceral_fat: Optional[conint(ge=0)]
    date: date
    user: Union[UserDto, UUID]

    def __init__(self, **kwargs):
        if "user" not in kwargs:
            kwargs["user"] = kwargs["user_id"]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
