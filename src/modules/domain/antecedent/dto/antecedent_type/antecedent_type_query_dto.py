from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllAntecedentTypeQueryDto(BaseModel):
    description: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByAntecedentTypeQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
