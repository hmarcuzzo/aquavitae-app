from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllTypeOfMealQueryDto(BaseModel):
    description: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByTypeOfMealQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    calories_percentage: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    lipids_percentage: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    proteins_percentage: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    carbohydrates_percentage: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
