from uuid import UUID

from pydantic import BaseModel, Extra, Field


class CreateFoodCanEatAtDto(BaseModel):
    type_of_meal_id: UUID = Field(alias="type_of_meal")
    food_id: UUID = Field(alias="food")

    class Config:
        extra = Extra.forbid
