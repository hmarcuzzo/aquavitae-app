from typing import Union
from uuid import UUID

from pydantic import condecimal, constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto


class FoodDto(BaseDto):
    description: constr(max_length=255)
    proteins: condecimal(decimal_places=2)
    lipids: condecimal(decimal_places=2)
    carbohydrates: condecimal(decimal_places=2)
    energy_value: condecimal(decimal_places=2)
    potassium: condecimal(decimal_places=2)
    phosphorus: condecimal(decimal_places=2)
    sodium: condecimal(decimal_places=2)
    food_category: Union[FoodCategoryDto, UUID]

    def __init__(self, **kwargs):
        if "food_category" not in kwargs:
            kwargs["food_category"] = kwargs["food_category_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
