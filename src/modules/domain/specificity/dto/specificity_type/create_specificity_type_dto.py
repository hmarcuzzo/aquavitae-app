from uuid import UUID

from pydantic import BaseModel, constr, Extra, condecimal, Field


class CreateSpecificityTypeDto(BaseModel):
    description: constr(max_length=1000)

    class Config:
        extra = Extra.forbid
