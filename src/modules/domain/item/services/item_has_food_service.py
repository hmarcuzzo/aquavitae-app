from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.types.update_result_type import UpdateResult
from src.modules.domain.item.dto.item_has_food.create_item_has_food_dto import CreateItemHasFoodDto
from src.modules.domain.item.dto.item_has_food.item_has_food_dto import ItemHasFoodDto
from src.modules.domain.item.dto.item_has_food.update_item_has_food_dto import UpdateItemHasFoodDto
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.entities.item_has_food_entity import ItemHasFood
from src.modules.domain.item.repositories.item_has_food_repository import ItemHasFoodRepository
from src.modules.domain.item.repositories.item_repository import ItemRepository


class ItemHasFoodService:
    def __init__(self):
        self.item_has_food_repository = ItemHasFoodRepository()

    # ---------------------- PUBLIC METHODS ----------------------

    # ---------------------- INTERFACE METHODS ----------------------
    async def create_item_has_food_interface(
        self, item_has_foods: List[CreateItemHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
        db.begin_nested()
        return await self._create_item_has_food(item_has_foods, db)

    async def update_item_has_food_interface(
        self, update_item_has_foods: List[UpdateItemHasFoodDto], db: Session
    ) -> Optional[UpdateResult]:
        return await self._update_item_has_food(update_item_has_foods, db)

    # ---------------------- PRIVATE METHODS ----------------------
    async def _create_item_has_food(
        self, item_has_foods: List[CreateItemHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
        new_item_has_foods: List[ItemHasFood] = []
        for food in item_has_foods:
            tmp_item_has_food = await self.item_has_food_repository.create(food, db)
            new_item_has_foods.append(tmp_item_has_food)

        new_item_has_foods = await self.item_has_food_repository.save(new_item_has_foods, db)
        return [ItemHasFoodDto(**item_has_food.__dict__) for item_has_food in new_item_has_foods]

    async def _update_item_has_food(
        self, update_item_has_foods: List[UpdateItemHasFoodDto], db: Session
    ) -> Optional[UpdateResult]:
        item = await ItemRepository().find_one_or_fail(
            {"where": Item.id == update_item_has_foods[0].item_id, "relations": ["foods"]}, db
        )

        response: UpdateResult = UpdateResult(raw=[], affected=0, generatedMaps=[])

        foods_updated = []
        for item_food in item.foods:
            db.begin_nested()
            updated = False
            for new_food in update_item_has_foods:
                # Update foods in the new foods list
                if item_food.food_id == new_food.food_id:
                    updated = True
                    foods_updated.append(new_food)
                    response["affected"] += (
                        await self.item_has_food_repository.update(str(item_food.id), new_food, db)
                    )["affected"]

            # Delete foods not in the new foods list
            if not updated:
                response["affected"] += (
                    await self.item_has_food_repository.soft_delete(str(item_food.id), db)
                )["affected"]

        # Create new foods in update method
        db.begin_nested()
        response["affected"] += len(
            await self._create_item_has_food(
                [new_food for new_food in update_item_has_foods if new_food not in foods_updated],
                db,
            )
        )

        return response
