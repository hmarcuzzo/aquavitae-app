from typing import Optional, Union
from uuid import UUID

from pydantic import condecimal, confloat, constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto


class FoodCanEatAtDto(BaseDto):
    type_of_meal: Optional[Union[TypeOfMealDto, UUID]]
    food: Optional[Union[FoodDto, UUID]]

    def __init__(self, **kwargs):
        if "type_of_meal" not in kwargs and "type_of_meal_id" in kwargs:
            kwargs["type_of_meal"] = kwargs["type_of_meal_id"]

        if "food" not in kwargs and "food_id" in kwargs:
            kwargs["food"] = kwargs["food_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
