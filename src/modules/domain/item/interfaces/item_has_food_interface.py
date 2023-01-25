from typing import List, Optional

from sqlalchemy.orm import Session

from src.modules.domain.item.dto.item.create_item_dto import ListHasFoodDto
from src.modules.domain.item.dto.item_has_food.create_item_has_food_dto import CreateItemHasFoodDto
from src.modules.domain.item.dto.item_has_food.item_has_food_dto import ItemHasFoodDto
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.services.item_has_food_service import ItemHasFoodService


class ItemHasFoodInterface:
    def __init__(self):
        self.item_has_food_service = ItemHasFoodService()

    async def create_item_has_food(
        self, item: Item, foods: List[ListHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
        return await self.item_has_food_service.create_item_has_food_interface(
            [
                CreateItemHasFoodDto(
                    **{"amount_grams": food.amount_grams, "food": food.food_id, "item": item.id}
                )
                for food in foods
            ],
            db,
        )
