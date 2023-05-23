from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class CreateAntecedentDto(BaseModel):
    description: constr(max_length=255)
    antecedent_type_id: UUID = Field(alias="antecedent_type")
    user_id: UUID = Field(alias="user")

    class Config:
        extra = Extra.forbid
