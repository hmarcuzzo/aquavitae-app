from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllUserQueryDto(BaseModel):
    email: Optional[constr()]
    role: Optional[constr()]
    last_access: Optional[constr()]

    class Config:
        extra = Extra.forbid


class OrderByUserQueryDto(BaseModel):
    email: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    role: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    last_access: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
