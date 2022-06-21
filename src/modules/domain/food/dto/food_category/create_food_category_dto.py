from typing import Optional
from uuid import UUID

from pydantic import BaseModel, conint, constr, Extra, Field


class CreateFoodCategoryDto(BaseModel):
    description: constr(max_length=255)
    level: conint()
    food_category_id: Optional[UUID] = Field(alias="food_category")

    class Config:
        extra = Extra.forbid
