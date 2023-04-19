from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.item_can_eat_at.create_item_can_eat_at_dto import (
    CreateItemCanEatAtDto,
)
from src.modules.domain.meal.dto.item_can_eat_at.item_can_eat_at_dto import ItemCanEatAtDto
from src.modules.domain.meal.entities.item_can_eat_at_entity import ItemCanEatAt
from src.modules.domain.meal.services.item_can_eat_at_service import ItemCanEatAtService


class ItemCanEatAtInterface:
    def __init__(self):
        self.item_can_eat_at_service = ItemCanEatAtService()

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, food_id: UUID, db_session
    ) -> Optional[ItemCanEatAt]:
        return await self.item_can_eat_at_service.find_one_can_eat_at(
            meal_type_id, food_id, db_session
        )

    async def create_food_can_eat_at(
        self,
        type_of_meal_id: UUID,
        item_id: UUID,
        db: Session,
    ) -> Optional[ItemCanEatAtDto]:
        return await self.item_can_eat_at_service.create_item_can_eat_at(
            CreateItemCanEatAtDto(
                **{
                    "type_of_meal": type_of_meal_id,
                    "item": item_id,
                }
            ),
            db,
        )
