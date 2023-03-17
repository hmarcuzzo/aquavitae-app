from typing import List, Optional

from pydantic import BaseModel, conlist, constr, Extra, Field

from src.modules.domain.item.dto.item.list_has_food_dto import ListHasFoodDto


class UpdateItemDto(BaseModel):
    description: Optional[constr(max_length=255)]
    foods: Optional[conlist(ListHasFoodDto, min_items=1)]

    class Config:
        extra = Extra.forbid
