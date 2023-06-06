from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class UpdateAntecedentDto(BaseModel):
    description: Optional[constr(max_length=255)]
    antecedent_type_id: Optional[UUID] = Field(alias="antecedent_type")

    class Config:
        extra = Extra.forbid
