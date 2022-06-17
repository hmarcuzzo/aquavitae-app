from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.food.dto.food.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.dto.food.update_food_dto import UpdateFoodDto
from src.modules.domain.food.repositories.food_repository import FoodRepository


class FoodService:
    def __init__(self):
        self.food_repository = FoodRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_food(self, food_dto: CreateFoodDto, db: Session) -> Optional[FoodDto]:
        new_food = await self.food_repository.create(db, food_dto)

        new_food = await self.food_repository.save(db, new_food)
        return FoodDto(**new_food.__dict__)

    async def get_all_food_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[FoodDto]]:
        [all_food, total] = await self.food_repository.find_and_count(db, pagination)

        return create_pagination_response_dto(
            [FoodDto(**food.__dict__) for food in all_food],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def find_one_food(self, food_id: str, db: Session) -> Optional[FoodDto]:
        food = await self.food_repository.find_one_or_fail(db, food_id)

        return FoodDto(**food.__dict__)

    async def delete_food(self, food_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.food_repository.soft_delete(db, food_id)

    async def update_food(
        self, id: str, update_food_dto: UpdateFoodDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.food_repository.update(db, id, update_food_dto)
