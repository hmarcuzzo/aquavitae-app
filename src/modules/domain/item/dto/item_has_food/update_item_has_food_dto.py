from pydantic import Extra

from src.modules.domain.item.dto.item_has_food.create_item_has_food_dto import CreateItemHasFoodDto


class UpdateItemHasFoodDto(CreateItemHasFoodDto):
    class Config:
        extra = Extra.forbid
