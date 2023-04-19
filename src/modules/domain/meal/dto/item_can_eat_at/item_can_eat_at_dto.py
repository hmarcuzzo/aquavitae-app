from typing import Optional, Union
from uuid import UUID

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto


class ItemCanEatAtDto(BaseDto):
    type_of_meal: Optional[Union[TypeOfMealDto, UUID]]
    item: Optional[Union[ItemDto, UUID]]

    def __init__(self, **kwargs):
        if "type_of_meal" not in kwargs and "type_of_meal_id" in kwargs:
            kwargs["type_of_meal"] = kwargs["type_of_meal_id"]

        if "item" not in kwargs and "item_id" in kwargs:
            kwargs["item"] = kwargs["item_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
