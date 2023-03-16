from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.meal.dto.type_of_meal.create_type_of_meal_dto import CreateTypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.update_type_of_meal_dto import UpdateTypeOfMealDto
from src.modules.domain.meal.entities.type_of_meal_entity import TypeOfMeal
from src.modules.domain.meal.repositories.type_of_meal_repository import TypeOfMealRepository


class TypeOfMealService:
    def __init__(self):
        self.type_of_meal_repository = TypeOfMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_type_of_meal(
        self, type_of_meal_dto: CreateTypeOfMealDto, db: Session
    ) -> Optional[TypeOfMealDto]:
        new_type_of_meal = await self.type_of_meal_repository.create(type_of_meal_dto, db)

        new_type_of_meal = self.type_of_meal_repository.save(new_type_of_meal, db)
        return TypeOfMealDto(**new_type_of_meal.__dict__)

    async def find_one_type_of_meal(self, id: str, db: Session):
        type_of_meal = await self.type_of_meal_repository.find_one_or_fail(
            {"where": TypeOfMeal.id == id}, db
        )

        return TypeOfMealDto(**type_of_meal.__dict__)

    async def delete_type_of_meal(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.type_of_meal_repository.soft_delete(id, db)

    async def update_type_of_meal(
        self, id: str, update_type_of_meal_dto: UpdateTypeOfMealDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.type_of_meal_repository.update(id, update_type_of_meal_dto, db)

    async def get_all_type_of_meal_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[TypeOfMealDto]]:
        [all_type_of_meal, total] = await self.type_of_meal_repository.find_and_count(
            pagination, db
        )

        return create_pagination_response_dto(
            [TypeOfMealDto(**type_of_meal.__dict__) for type_of_meal in all_type_of_meal],
            total,
            pagination["skip"],
            pagination["take"],
        )

    # ---------------------- INTERFACE METHODS ----------------------
    async def find_one_type_of_meal_by_description(
        self, description: str, db: Session
    ) -> Optional[TypeOfMealDto]:
        type_of_meal = await self.type_of_meal_repository.find_one_or_fail(
            {
                "where": TypeOfMeal.description == description,
            },
            db,
        )

        return TypeOfMealDto(**type_of_meal.__dict__)
