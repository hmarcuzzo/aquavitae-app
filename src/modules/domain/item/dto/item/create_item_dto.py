from pydantic import BaseModel, conlist, constr, Extra

from src.modules.domain.item.dto.item.list_has_food_dto import ListHasFoodDto


class CreateItemDto(BaseModel):
    description: constr(max_length=255)
    foods: conlist(ListHasFoodDto, min_items=1)

    class Config:
        extra = Extra.forbid
