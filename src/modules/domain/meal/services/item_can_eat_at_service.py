from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.item_can_eat_at.create_item_can_eat_at_dto import (
    CreateItemCanEatAtDto,
)
from src.modules.domain.meal.dto.item_can_eat_at.item_can_eat_at_dto import ItemCanEatAtDto
from src.modules.domain.meal.entities.item_can_eat_at_entity import ItemCanEatAt
from src.modules.domain.meal.repositories.item_can_eat_at_repository import ItemCanEatAtRepository


class ItemCanEatAtService:
    def __init__(self):
        self.item_can_eat_at_repository = ItemCanEatAtRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_item_can_eat_at(
        self, food_can_eat_at_dto: CreateItemCanEatAtDto, db: Session
    ) -> Optional[ItemCanEatAtDto]:
        new_food_can_eat_at = await self.item_can_eat_at_repository.create(food_can_eat_at_dto, db)

        new_food_can_eat_at = self.item_can_eat_at_repository.save(new_food_can_eat_at, db)
        return ItemCanEatAtDto(**new_food_can_eat_at.__dict__)

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, item_id: UUID, db_session
    ) -> Optional[ItemCanEatAt]:
        return await self.item_can_eat_at_repository.find_one_or_fail(
            {
                "where": [
                    ItemCanEatAt.type_of_meal_id == meal_type_id,
                    ItemCanEatAt.item_id == item_id,
                ]
            },
            db_session,
        )
