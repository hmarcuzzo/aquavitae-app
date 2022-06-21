from __future__ import annotations

from typing import Union
from uuid import UUID

from pydantic import conint, constr, Field

from src.core.common.dto.base_dto import BaseDto


class FoodCategoryDto(BaseDto):
    description: constr(max_length=255)
    level: conint()
    food_category: Union[FoodCategoryDto, UUID] = Field(default=None)

    def __init__(self, **kwargs):
        if "food_category" not in kwargs:
            kwargs["food_category"] = kwargs["food_category_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True


FoodCategoryDto.update_forward_refs()
