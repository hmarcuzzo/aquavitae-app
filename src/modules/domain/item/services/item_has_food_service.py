from typing import List, Optional

from sqlalchemy.orm import Session

from src.modules.domain.item.dto.item_has_food.create_item_has_food_dto import CreateItemHasFoodDto
from src.modules.domain.item.dto.item_has_food.item_has_food_dto import ItemHasFoodDto
from src.modules.domain.item.entities.item_has_food_entity import ItemHasFood
from src.modules.domain.item.repositories.item_has_food_repository import ItemHasFoodRepository


class ItemHasFoodService:
    def __init__(self):
        self.item_has_food_repository = ItemHasFoodRepository()

    # ---------------------- PUBLIC METHODS ----------------------

    # ---------------------- INTERFACE METHODS ----------------------
    async def create_item_has_food_interface(
        self, item_has_foods_dto: List[CreateItemHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
        db.begin_nested()
        return await self._create_item_has_food(item_has_foods_dto, db)

    # ---------------------- PRIVATE METHODS ----------------------
    async def _create_item_has_food(
        self, item_has_foods_dto: List[CreateItemHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
        new_item_has_foods: List[ItemHasFood] = []
        for food in item_has_foods_dto:
            tmp_item_has_food = await self.item_has_food_repository.create(food, db)
            new_item_has_foods.append(tmp_item_has_food)

        new_item_has_foods = await self.item_has_food_repository.save(new_item_has_foods, db)
        return [ItemHasFoodDto(**item_has_food.__dict__) for item_has_food in new_item_has_foods]
