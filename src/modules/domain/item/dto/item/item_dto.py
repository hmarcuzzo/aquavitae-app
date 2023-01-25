from typing import List, Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.item.dto.item_has_food.item_has_food_dto import ItemHasFoodDto


class ItemDto(BaseDto):
    description: constr(max_length=255)
    foods: Optional[List[Union[ItemHasFoodDto, UUID]]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
