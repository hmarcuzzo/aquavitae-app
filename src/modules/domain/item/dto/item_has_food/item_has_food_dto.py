from typing import Optional, Union
from uuid import UUID

from pydantic import condecimal

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.food.dto.food.food_dto import FoodDto


class ItemHasFoodDto(BaseDto):
    amount_grams: condecimal(decimal_places=2)
    food: Optional[Union[FoodDto, UUID]]

    def __init__(self, **kwargs):
        if "food" not in kwargs and "food_id" in kwargs:
            kwargs["food"] = kwargs["food_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True


ItemHasFoodDto.update_forward_refs()
