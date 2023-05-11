from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.item.dto.item.list_has_food_dto import ListHasFoodDto
from src.modules.domain.item.services.item_service import ItemService


class ItemInterface:
    def __init__(self):
        self.item_service = ItemService()

    async def find_one_item_by_description(
        self, description: str, db: Session
    ) -> Optional[ItemDto]:
        return await self.item_service.find_one_item_by_description(description, db)

    async def create_item(
        self,
        description: str,
        foods: List[ListHasFoodDto],
        can_eat_at: List[UUID],
        db: Session,
    ) -> Optional[ItemDto]:
        return await self.item_service.create_item(
            CreateItemDto(description=description, foods=foods, can_eat_at=can_eat_at), db
        )
