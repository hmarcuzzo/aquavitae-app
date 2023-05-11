from typing import List, Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.item.dto.item_has_food.item_has_food_dto import ItemHasFoodDto
from src.modules.domain.meal.dto.item_can_eat_at.item_can_eat_at_dto import ItemCanEatAtDto


class ItemDto(BaseDto):
    description: constr(max_length=255)
    foods: Optional[Union[List[ItemHasFoodDto], List[UUID]]]
    can_eat_at: Optional[Union[List[ItemCanEatAtDto], List[UUID]]]

    def __init__(self, **kwargs):
        if "can_eat_at" in kwargs and not all(
            isinstance(can_eat_at, dict) for can_eat_at in kwargs["can_eat_at"]
        ):
            kwargs["can_eat_at"] = [
                ItemCanEatAtDto(**item.__dict__) for item in kwargs["can_eat_at"]
            ]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
