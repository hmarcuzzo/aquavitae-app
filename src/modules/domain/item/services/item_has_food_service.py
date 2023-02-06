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
from src.modules.infrastructure.database.control_transaction import keep_nested_transaction


class ItemHasFoodService:
    def __init__(self):
        self.item_has_food_repository = ItemHasFoodRepository()

    # ---------------------- INTERFACE METHODS ----------------------
    async def create_item_has_food_interface(
        self, item_has_foods: List[CreateItemHasFoodDto], db: Session
    ) -> Optional[List[ItemHasFoodDto]]:
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

        new_item_has_foods = self.item_has_food_repository.save(new_item_has_foods, db)
        return [ItemHasFoodDto(**item_has_food.__dict__) for item_has_food in new_item_has_foods]

    async def _update_item_has_food(
        self, update_item_has_foods: List[UpdateItemHasFoodDto], db: Session
    ) -> Optional[UpdateResult]:
        item = await ItemRepository().find_one_or_fail(
            {"where": Item.id == update_item_has_foods[0].item_id, "relations": ["foods"]}, db
        )
        item_foods_id = {item_food.food_id: {item_food.id} for item_food in item.foods}

        response = UpdateResult(raw=[], affected=0, generatedMaps=[])

        with keep_nested_transaction(db):
            for new_food in update_item_has_foods:
                if new_food.food_id in item_foods_id:
                    # Update foods in the new foods list
                    response["affected"] += (
                        await self.item_has_food_repository.update(
                            str(item_foods_id[new_food.food_id].pop()), new_food, db
                        )
                    )["affected"]
                    del item_foods_id[new_food.food_id]

                else:
                    # Create new foods in update method
                    response["affected"] += len(await self._create_item_has_food([new_food], db))

            # Delete foods not in the new foods list
            if len(item_foods_id) > 0:
                for food_id in item_foods_id:
                    response["affected"] += (
                        await self.item_has_food_repository.soft_delete(
                            str(item_foods_id[food_id].pop()), db
                        )
                    )["affected"]

        db.commit()
        return response
