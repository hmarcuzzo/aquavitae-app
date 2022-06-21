from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.food.dto.food_category.create_food_category_dto import (
    CreateFoodCategoryDto,
)
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto
from src.modules.domain.food.dto.food_category.update_food_category_dto import (
    UpdateFoodCategoryDto,
)
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.repositories.food_category_repository import (
    FoodCategoryRepository,
)


class FoodCategoryService:
    def __init__(self):
        self.food_category_repository = FoodCategoryRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_food_category(
        self, food_category_dto: CreateFoodCategoryDto, db: Session
    ) -> Optional[FoodCategoryDto]:
        new_food_category = await self.food_category_repository.create(
            db, food_category_dto
        )

        new_food_category = await self.food_category_repository.save(
            db, new_food_category
        )
        return FoodCategoryDto(**new_food_category.__dict__)

    async def get_all_food_category_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[FoodCategoryDto]]:
        pagination["relations"] = ["food_category"]
        [
            all_food_categories,
            total,
        ] = await self.food_category_repository.find_and_count(db, pagination)

        return create_pagination_response_dto(
            [
                FoodCategoryDto(**food_category.__dict__)
                for food_category in all_food_categories
            ],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def find_one_food_category(
        self, food_category_id: str, db: Session
    ) -> Optional[FoodCategoryDto]:
        food_category = await self.food_category_repository.find_one_or_fail(
            db,
            {
                "where": FoodCategory.id == food_category_id,
                "relations": ["food_category"],
            },
        )

        return FoodCategoryDto(**food_category.__dict__)

    async def update_food_category(
        self, id: str, update_food_category_dto: UpdateFoodCategoryDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.food_category_repository.update(
            db, id, update_food_category_dto
        )

    async def delete_food_category(
        self, food_category_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.food_category_repository.soft_delete(db, food_category_id)
