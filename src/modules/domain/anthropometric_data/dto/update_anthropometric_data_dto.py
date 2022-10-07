from datetime import date
from typing import Optional

from pydantic import BaseModel, confloat, conint, Extra


class UpdateAnthropometricDataDto(BaseModel):
    weight: Optional[confloat(ge=0)]
    height: Optional[conint(ge=0)]
    waist_circumference: Optional[conint(ge=0)]
    fat_mass: Optional[confloat(ge=0)]
    muscle_mass: Optional[confloat(ge=0)]
    bone_mass: Optional[confloat(ge=0)]
    body_water: Optional[confloat(ge=0)]
    basal_metabolism: Optional[conint(ge=0)]
    visceral_fat: Optional[conint(ge=0)]
    date: Optional[date]
    body_photo: Optional[bytes]

    class Config:
        extra = Extra.forbid


class UserUpdateAnthropometricDataDto(BaseModel):
    weight: Optional[confloat(ge=0)]

    class Config:
        extra = Extra.forbid
