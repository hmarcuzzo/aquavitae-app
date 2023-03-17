from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.food_can_eat_at.create_food_can_eat_at_dto import (
    CreateFoodCanEatAtDto,
)
from src.modules.domain.meal.dto.food_can_eat_at.food_can_eat_at_dto import FoodCanEatAtDto
from src.modules.domain.meal.entities.food_can_eat_at_entity import FoodCanEatAt
from src.modules.domain.meal.repositories.food_can_eat_at_repository import FoodCanEatAtRepository


class FoodCanEatAtService:
    def __init__(self):
        self.food_can_eat_at_repository = FoodCanEatAtRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_food_can_eat_at(
        self, food_can_eat_at_dto: CreateFoodCanEatAtDto, db: Session
    ) -> Optional[FoodCanEatAtDto]:
        new_food_can_eat_at = await self.food_can_eat_at_repository.create(food_can_eat_at_dto, db)

        new_food_can_eat_at = self.food_can_eat_at_repository.save(new_food_can_eat_at, db)
        return FoodCanEatAtDto(**new_food_can_eat_at.__dict__)

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, food_id: UUID, db_session
    ) -> Optional[FoodCanEatAt]:
        return await self.food_can_eat_at_repository.find_one_or_fail(
            {
                "where": [
                    FoodCanEatAt.type_of_meal_id == meal_type_id,
                    FoodCanEatAt.food_id == food_id,
                ]
            },
            db_session,
        )
