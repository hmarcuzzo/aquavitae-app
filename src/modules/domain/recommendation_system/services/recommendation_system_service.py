from datetime import date, timedelta
from typing import List

import pandas as pd
from cachetools import TTLCache
from sqlalchemy.orm import Session

from src.core.types.exceptions_type import BadRequestException
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.nutritional_plan.interfaces.nutritional_plan_interface import (
    NutritionalPlanInterface,
)
from src.modules.domain.recommendation_system.dto.user_preferences_table_dto import (
    DetailedUserPreferencesTable,
)
from src.modules.domain.recommendation_system.interfaces.find_user_food_preferences_interface import (
    FindUserFoodPreferencesInterface,
)
from src.modules.domain.recommendation_system.repositories.recommendation_system_repository import (
    RecommendationSystemRepository,
)

all_food_cache = TTLCache(maxsize=1, ttl=60 * 60)
user_food_preference_cache = TTLCache(maxsize=100, ttl=60 * 60)


def all_foods_cache_key(db: Session):
    return f"all_foods_{db.get_bind().url.database}_{db.get_bind().dialect.name}"


class RecommendationSystemService:
    def __init__(self):
        self.rs_repository = RecommendationSystemRepository()
        self.nutritional_plan_interface = NutritionalPlanInterface()
        self.find_user_food_preferences_interface = FindUserFoodPreferencesInterface()

    # ---------------------- PUBLIC METHODS ----------------------
    async def complete_nutritional_plan(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ):
        types_of_meal_plan = self.rs_repository.get_types_of_meal_plan(nutritional_plan_id, db)
        if len(types_of_meal_plan) == 0:
            raise BadRequestException(
                "It is necessary that the nutritional plan has marked which type of meals it has."
            )
        nutritional_plan = await self.nutritional_plan_interface.get_nutritional_plan(
            nutritional_plan_id, db
        )
        user_food_preference = await self.get_user_food_preferences(
            user_id, nutritional_plan_id, available, force_reload, db
        )
        self.__complete_nutritional_plan(nutritional_plan, user_food_preference, types_of_meal_plan)

    async def get_user_food_preferences(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ) -> List[DetailedUserPreferencesTable]:
        return await self.find_user_food_preferences_interface.get_user_food_preferences(
            user_id, nutritional_plan_id, available, force_reload, db
        )

    # ---------------------- PRIVATE METHODS ----------------------
    def __complete_nutritional_plan(
        self,
        nutritional_plan: NutritionalPlan,
        user_food_preference: List[DetailedUserPreferencesTable],
        types_of_meal_plan: List[dict],
    ):
        date_list = RecommendationSystemService.__get_date_range(nutritional_plan)
        # all_consumable_items =

        foods_by_type_of_meal = {}
        for type_of_meal in types_of_meal_plan:
            foods_by_type_of_meal[type_of_meal["type_of_meal_id"]] = [
                food for food in user_food_preference if food.meal_time == type_of_meal["meal_time"]
            ]

        for day in date_list:
            pass

    @staticmethod
    def __get_date_range(nutritional_plan: NutritionalPlan) -> List[date]:
        meals_df = pd.DataFrame.from_records(
            [meal.__dict__ for meal in nutritional_plan.nutritional_plan_meals]
        )

        first_date = meals_df.sort_values("meal_date")["meal_date"][0]
        return (
            pd.date_range(start=first_date, end=nutritional_plan.validate_date).to_period().tolist()
        )
