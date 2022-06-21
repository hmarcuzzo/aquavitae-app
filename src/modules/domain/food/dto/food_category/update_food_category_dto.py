from typing import Optional
from uuid import UUID

from pydantic import BaseModel, conint, constr, Extra, Field


class UpdateFoodCategoryDto(BaseModel):
    description: Optional[constr(max_length=255)]
    level: Optional[conint()]
    food_category_id: Optional[UUID] = Field(alias="food_category")

    class Config:
        extra = Extra.forbid
