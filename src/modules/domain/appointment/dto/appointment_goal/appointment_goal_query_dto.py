from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllAppointmentGoalQueryDto(BaseModel):
    description: Optional[constr(max_length=1000)]

    class Config:
        extra = Extra.forbid


class OrderByAppointmentGoalQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
