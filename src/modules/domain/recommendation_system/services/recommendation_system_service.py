from typing import List

from sqlalchemy.orm import Session

from src.core.types.exceptions_type import BadRequestException
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.interfaces.food_interface import FoodInterface
from src.modules.domain.nutritional_plan.interfaces.nutritional_plan_interface import (
    NutritionalPlanInterface,
)
from src.modules.domain.recommendation_system.repositories.recommendation_system_repository import (
    RecommendationSystemRepository,
)


class RecommendationSystemService:
    def __init__(self):
        self.rs_repository = RecommendationSystemRepository()
        self.food_interface = FoodInterface()
        self.nutritional_plan_interface = NutritionalPlanInterface()

    # ---------------------- PUBLIC METHODS ----------------------
    async def complete_nutritional_plan(self, user_id: str, nutritional_plan_id: str, db: Session):
        types_of_meal_plan = self.rs_repository.get_types_of_meal_plan(nutritional_plan_id, db)
        if len(types_of_meal_plan) == 0:
            raise BadRequestException(
                "It is necessary that the nutritional plan has marked which type of meals it has."
            )
        nutritional_plan = await self.nutritional_plan_interface.get_nutritional_plan(
            nutritional_plan_id, db
        )
        pass

    async def user_food_preferences(
        self, user_id: str, nutritional_plan_id: str, available: bool, db: Session
    ):
        all_foods = await self.food_interface.get_all_food(db)

        await self._generate_preference_ranking(user_id, all_foods, db)

        if available:
            cant_consume_foods = [
                FoodDto(**item)
                for item in self.rs_repository.get_user_cant_consume_food_ids(
                    user_id, nutritional_plan_id, db
                )
            ]

    # ---------------------- PRIVATE METHODS ----------------------
    async def _generate_preference_ranking(
        self, user_id: str, all_foods: List[FoodDto], db: Session
    ):
        food_preferences = self.rs_repository.get_user_food_preferences(user_id, db)
        user_consumption_history = self.rs_repository.get_user_consumption_history(user_id, db)
