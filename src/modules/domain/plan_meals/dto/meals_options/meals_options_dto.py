from typing import Optional, Union
from uuid import UUID

from pydantic import confloat

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.nutritional_plan.dto.nutritional_plan_dto import NutritionalPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.meals_of_plan_dto import MealsOfPlanDto


class MealsOptionsDto(BaseDto):
    amount: confloat(ge=0.5, le=3, multiple_of=0.5)
    suggested_by_system: Optional[bool]
    item: Union[NutritionalPlanDto, UUID]
    nutritional_plan_has_meal: Optional[Union[MealsOfPlanDto, UUID]]

    def __init__(self, **kwargs):
        if "item" not in kwargs and "item_id" in kwargs:
            kwargs["item"] = kwargs["item_id"]

        if "nutritional_plan_has_meal" not in kwargs and "nutritional_plan_has_meal_id" in kwargs:
            kwargs["nutritional_plan_has_meal"] = kwargs["nutritional_plan_has_meal_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
