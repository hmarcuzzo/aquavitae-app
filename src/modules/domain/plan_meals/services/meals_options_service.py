from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.plan_meals.dto.meals_options.create_meals_options_dto import (
    CreateMealsOptionsDto,
)
from src.modules.domain.plan_meals.dto.meals_options.meals_options_dto import MealsOptionsDto
from src.modules.domain.plan_meals.repositories.meals_options_repository import (
    MealsOptionsRepository,
)


class MealsOptionsService:
    def __init__(self):
        self.meals_options_repository = MealsOptionsRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_meal_option(
        self, create_meals_options_dto: CreateMealsOptionsDto, db: Session
    ) -> Optional[MealsOptionsDto]:
        new_meal_option = await self.meals_options_repository.create(create_meals_options_dto, db)

        new_meal_option = self.meals_options_repository.save(new_meal_option, db)
        return MealsOptionsDto(**new_meal_option.__dict__)
