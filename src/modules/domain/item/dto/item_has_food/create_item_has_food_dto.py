from uuid import UUID

from pydantic import BaseModel, condecimal, Extra, Field

from src.core.constants.default_values import DEFAULT_AMOUNT_GRAMS


class CreateItemHasFoodDto(BaseModel):
    amount_grams: condecimal(decimal_places=2) = Field(default=DEFAULT_AMOUNT_GRAMS)
    food_id: UUID = Field(alias="food")
    item_id: UUID = Field(alias="item")

    class Config:
        extra = Extra.forbid
