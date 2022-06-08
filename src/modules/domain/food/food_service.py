from typing import Optional

from sqlalchemy.orm import Session

from src.core.types.update_result_type import UpdateResult
from src.modules.domain.food.dto.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.update_food_dto import UpdateFoodDto
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.food_repository import FoodRepository


class FoodService:
    def __init__(self):
        self.food_repository = FoodRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_food(self, food_dto: CreateFoodDto, db: Session) -> Optional[Food]:
        new_food = await self.food_repository.create(db, food_dto)

        return await self.food_repository.save(db, new_food)

    async def find_one_food(self, food_id: str, db: Session) -> Optional[Food]:
        food = await self.food_repository.find_one_or_fail(db, food_id)

        return food

    async def delete_food(self, food_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.food_repository.soft_delete(db, food_id)

    async def update_food(self, id: str, update_food_dto: UpdateFoodDto, db: Session) -> Optional[UpdateResult]:
        return await self.food_repository.update(db, id, update_food_dto)

    # ---------------------- PRIVATE METHODS ----------------------
