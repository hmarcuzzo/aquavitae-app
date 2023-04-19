from uuid import UUID

from pydantic import BaseModel, Extra, Field


class CreateItemCanEatAtDto(BaseModel):
    type_of_meal_id: UUID = Field(alias="type_of_meal")
    item_id: UUID = Field(alias="item")

    class Config:
        extra = Extra.forbid
