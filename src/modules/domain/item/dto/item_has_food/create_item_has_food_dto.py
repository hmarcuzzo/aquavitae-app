from uuid import UUID

from pydantic import BaseModel, condecimal, Extra, Field


class CreateItemHasFoodDto(BaseModel):
    amount_grams: condecimal(decimal_places=2)
    food_id: UUID = Field(alias="food")
    item_id: UUID = Field(alias="item")

    class Config:
        extra = Extra.forbid
