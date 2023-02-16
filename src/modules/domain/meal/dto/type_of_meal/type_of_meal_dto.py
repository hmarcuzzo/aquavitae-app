from typing import Optional, Union
from uuid import UUID

from pydantic import condecimal, confloat, constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto


class TypeOfMealDto(BaseDto):
    description: Optional[constr(max_length=255)]
    calories_percentage: Optional[confloat()]
    lipids_percentage: Optional[confloat()]
    proteins_percentage: Optional[confloat()]
    carbohydrates_percentage: Optional[confloat()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
