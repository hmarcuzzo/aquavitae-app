from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.interfaces.item_has_food_interface import ItemHasFoodInterface
from src.modules.domain.item.repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()
        self.item_has_food_interface = ItemHasFoodInterface()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_item(self, item_dto: CreateItemDto, db: Session) -> Optional[ItemDto]:
        try:
            db.begin_nested()
            response = await self._create_item(item_dto, db)
            db.commit()

            return response
        except Exception as e:
            db.rollback()
            raise e

    # ---------------------- INTERFACE METHODS ----------------------
    async def create_item_interface(
        self, item_dto: CreateItemDto, db: Session
    ) -> Optional[ItemDto]:
        db.begin_nested()
        return await self._create_item(item_dto, db)

    # ---------------------- PRIVATE METHODS ----------------------
    async def _create_item(self, item_dto: CreateItemDto, db: Session) -> Optional[ItemDto]:
        new_item = await self.item_repository.create(Item(description=item_dto.description), db)
        new_item = await self.item_repository.save(new_item, db)

        new_item_foods = await self.item_has_food_interface.create_item_has_food(
            new_item, item_dto.foods, db
        )

        response = ItemDto(**new_item.__dict__)
        response.foods = [new_item_food.food for new_item_food in new_item_foods]

        return response
