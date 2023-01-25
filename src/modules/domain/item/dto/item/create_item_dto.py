from typing import List
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field, condecimal

from src.core.constants.default_values import DEFAULT_AMOUNT_GRAMS


class ListHasFoodDto(BaseModel):
    amount_grams: condecimal(decimal_places=2) = Field(default=DEFAULT_AMOUNT_GRAMS)
    food_id: UUID = Field(alias="food")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        extra = Extra.forbid


class CreateItemDto(BaseModel):
    description: constr(max_length=255)
    foods: List[ListHasFoodDto]

    class Config:
        extra = Extra.forbid
