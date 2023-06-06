from datetime import time
from typing import Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto


class MealsOfPlanDto(BaseDto):
    description: constr(max_length=255)
    start_time: time
    end_time: time
    type_of_meal: Optional[Union[TypeOfMealDto, UUID]]

    def __init__(self, **kwargs):
        if "type_of_meal" not in kwargs and "type_of_meal_id" in kwargs:
            kwargs["type_of_meal"] = kwargs["type_of_meal_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
