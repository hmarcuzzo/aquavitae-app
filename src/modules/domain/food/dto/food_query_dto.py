from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllFoodQueryDto(BaseModel):
    description: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByFoodQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    proteins: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    lipids: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    carbohydrates: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    energy_value: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    potassium: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    phosphorus: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    sodium: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
