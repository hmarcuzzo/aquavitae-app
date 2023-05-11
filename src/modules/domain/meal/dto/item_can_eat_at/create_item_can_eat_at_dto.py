from uuid import UUID

from pydantic import BaseModel, conlist, Extra, Field


class CreateItemCanEatAtDto(BaseModel):
    type_of_meal_id: conlist(UUID, min_items=1) = Field(alias="type_of_meal")
    item_id: UUID = Field(alias="item")

    class Config:
        extra = Extra.forbid
