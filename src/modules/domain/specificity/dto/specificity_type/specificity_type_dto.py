from typing import Optional, Union
from uuid import UUID

from pydantic import condecimal, constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto


class SpecificityTypeDto(BaseDto):
    description: Optional[constr(max_length=1000)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
