from typing import Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.food.dto.food.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.services.food_service import FoodService
from src.modules.domain.plan_meals.dto.meals_options.create_meals_options_dto import (
    CreateMealsOptionsDto,
)
from src.modules.domain.plan_meals.dto.meals_options.meals_options_dto import MealsOptionsDto
from src.modules.domain.plan_meals.services.meals_options_service import MealsOptionsService


class MealsOptionsInterface:
    def __init__(self):
        self.meals_options_service = MealsOptionsService()

    async def create_meal_option(
        self,
        amount: float,
        suggested_by_system: bool,
        item_id: UUID,
        nutritional_plan_has_meal_id: UUID,
        db: Session,
    ) -> Optional[MealsOptionsDto]:
        return await self.meals_options_service.create_meal_option(
            CreateMealsOptionsDto(
                **{
                    "amount": amount,
                    "suggested_by_system": suggested_by_system,
                    "item": item_id,
                    "nutritional_plan_has_meal": nutritional_plan_has_meal_id,
                }
            ),
            db,
        )
