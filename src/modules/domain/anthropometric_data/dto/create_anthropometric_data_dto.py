from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, confloat, conint, Extra, Field


class CreateAnthropometricDataDto(BaseModel):
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
    user_id: UUID = Field(alias="user")

    class Config:
        extra = Extra.forbid
