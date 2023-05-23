from datetime import date
from typing import Optional, Union
from uuid import UUID

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.nutritional_plan.dto.nutritional_plan_dto import NutritionalPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.meals_of_plan_dto import MealsOfPlanDto


class NutritionalPlanHasMealDto(BaseDto):
    meal_date: date
    nutritional_plan: Optional[Union[NutritionalPlanDto, UUID]]
    meals_of_plan: Optional[Union[MealsOfPlanDto, UUID]]

    def __init__(self, **kwargs):
        if "nutritional_plan" not in kwargs and "nutritional_plan_id" in kwargs:
            kwargs["nutritional_plan"] = kwargs["nutritional_plan_id"]

        if "meals_of_plan" not in kwargs and "meals_of_plan_id" in kwargs:
            kwargs["meals_of_plan"] = kwargs["meals_of_plan_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
