from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.food_can_eat_at.create_food_can_eat_at_dto import (
    CreateFoodCanEatAtDto,
)
from src.modules.domain.meal.dto.food_can_eat_at.food_can_eat_at_dto import FoodCanEatAtDto
from src.modules.domain.meal.entities.food_can_eat_at_entity import FoodCanEatAt
from src.modules.domain.meal.services.food_can_eat_at_service import FoodCanEatAtService


class FoodCanEatAtInterface:
    def __init__(self):
        self.food_can_eat_at_service = FoodCanEatAtService()

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, food_id: UUID, db_session
    ) -> Optional[FoodCanEatAt]:
        return await self.food_can_eat_at_service.find_one_can_eat_at(
            meal_type_id, food_id, db_session
        )

    async def create_food_can_eat_at(
        self,
        type_of_meal_id: UUID,
        food_id: UUID,
        db: Session,
    ) -> Optional[FoodCanEatAtDto]:
        return await self.food_can_eat_at_service.create_food_can_eat_at(
            CreateFoodCanEatAtDto(
                **{
                    "type_of_meal": type_of_meal_id,
                    "food": food_id,
                }
            ),
            db,
        )
