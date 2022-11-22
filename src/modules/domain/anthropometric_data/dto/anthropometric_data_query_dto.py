from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllAnthropometricDataQueryDto(BaseModel):
    user_id: UUID

    class Config:
        extra = Extra.forbid


class OrderByAnthropometricDataQueryDto(BaseModel):
    weight: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    height: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    waist_circumference: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    fat_mass: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    muscle_mass: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    bone_mass: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    body_water: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    basal_metabolism: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    visceral_fat: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    date: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
