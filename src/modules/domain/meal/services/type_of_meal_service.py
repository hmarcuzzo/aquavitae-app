from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.type_of_meal.create_type_of_meal_dto import CreateTypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto
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
