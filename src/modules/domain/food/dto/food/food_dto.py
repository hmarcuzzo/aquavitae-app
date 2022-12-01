from typing import Optional, Union
from uuid import UUID

from pydantic import condecimal, constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto


class FoodDto(BaseDto):
    description: Optional[constr(max_length=255)]
    proteins: Optional[condecimal(decimal_places=2)]
    lipids: Optional[condecimal(decimal_places=2)]
    carbohydrates: Optional[condecimal(decimal_places=2)]
    energy_value: Optional[condecimal(decimal_places=2)]
    potassium: Optional[condecimal(decimal_places=2)]
    phosphorus: Optional[condecimal(decimal_places=2)]
    sodium: Optional[condecimal(decimal_places=2)]
    food_category: Optional[Union[FoodCategoryDto, UUID]]

    def __init__(self, **kwargs):
        if "food_category" not in kwargs and "food_category_id" in kwargs:
            kwargs["food_category"] = kwargs["food_category_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
