from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllPersonalDataQueryDto(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByPersonalDataQueryDto(BaseModel):
    first_name: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    last_name: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    birthday: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    occupation: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    food_history: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    bedtime: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    wake_up: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    activity_level: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
