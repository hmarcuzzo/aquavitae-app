from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import date
from typing import Dict, List
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session

from src.core.constants.default_values import DEFAULT_AMOUNT_GRAMS
from src.core.types.exceptions_type import BadRequestException, NotFoundException
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.nutritional_plan.interfaces.nutritional_plan_interface import (
    NutritionalPlanInterface,
)
from src.modules.domain.plan_meals.interfaces.nutritional_plan_has_meal_interface import (
    NutritionalPlanHasMealInterface,
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
from src.modules.infrastructure.database.control_transaction import keep_nested_transaction


class CompleteNutritionalPlanInterface:
    def __init__(self):
        self.rs_repository = RecommendationSystemRepository()
        self.nutritional_plan_interface = NutritionalPlanInterface()
        self.find_user_food_preferences_interface = FindUserFoodPreferencesInterface()
        self.nphm_interface = NutritionalPlanHasMealInterface()

    # ----------------- PUBLIC METHODS ----------------- #
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

        user_food_preferences = (
            await self.find_user_food_preferences_interface.get_user_food_preferences(
                user_id, nutritional_plan_id, available, force_reload, db
            )
        )

        allowed_food_ids = [food.id for food in user_food_preferences]
        allowed_items = self.rs_repository.get_allowed_items(allowed_food_ids, db)
        user_items_preference = self.__generate_item_table(user_food_preferences, allowed_items)

        # await self.__complete_nutritional_plan(
        #     nutritional_plan, user_items_preference, types_of_meal_plan, db
        # )

    # ----------------- PRIVATE METHODS ----------------- #
    @staticmethod
    def __generate_item_table(
        user_food_preferences: List[DetailedUserPreferencesTable], allowed_items: List[Item]
    ) -> pd.DataFrame:
        items_dataframe = pd.DataFrame.from_records([item.__dict__ for item in allowed_items])

        new_columns = {
            "score": 0,
            "proteins": 0,
            "lipids": 0,
            "carbohydrates": 0,
            "energy_value": 0,
            "can_eat_at": [[] for _ in range(len(items_dataframe))],
        }
        items_dataframe = items_dataframe.assign(**new_columns)

        food_preferences_dictionary = {
            food.id: pd.DataFrame.from_records([food.__dict__]) for food in user_food_preferences
        }

        with ThreadPoolExecutor() as executor:
            futures = []

            for current_item in allowed_items:
                submitted_future = executor.submit(
                    CompleteNutritionalPlanInterface.__set_item_data,
                    current_item,
                    items_dataframe,
                    food_preferences_dictionary,
                )
                futures.append(submitted_future)

            for future in as_completed(futures):
                # If the __set_item_data method raises an exception, it will be raised here
                pass

        return items_dataframe

    @staticmethod
    def __set_item_data(
        current_item: Item,
        items_dataframe: pd.DataFrame,
        food_preferences_dictionary: Dict[UUID, pd.DataFrame],
    ) -> None:
        for item_has_food in current_item.foods:
            food_id = item_has_food.food_id
            food_preferences = food_preferences_dictionary[food_id]
            amount_multiplier = item_has_food.amount_grams / DEFAULT_AMOUNT_GRAMS

            item_dataframe = items_dataframe[items_dataframe.id == current_item.id]

            # Add food score to item score
            items_dataframe.loc[item_dataframe.index, "score"] += food_preferences["score"].values

            # Update can_eat_at values
            can_eat_at_values = set(
                [can_eat_at.type_of_meal_id for can_eat_at in item_has_food.food.can_eat_at]
            )
            current_values = set(items_dataframe.at[item_dataframe.index[0], "can_eat_at"])
            items_dataframe.at[item_dataframe.index[0], "can_eat_at"] = list(
                current_values.union(can_eat_at_values)
            )

            # Add nutrient values to item nutrient values
            nutrient_columns = ["proteins", "lipids", "carbohydrates", "energy_value"]
            nutrient_values = (
                food_preferences[nutrient_columns].astype(float).values * amount_multiplier
            )
            items_dataframe.loc[item_dataframe.index, nutrient_columns] += nutrient_values

    async def __complete_nutritional_plan(
        self,
        nutritional_plan: NutritionalPlan,
        user_item_preference: pd.DataFrame,
        meal_plan: List[dict],
        db: Session,
    ):
        date_list = self.__get_date_range(nutritional_plan)
        adapted_meal_plan = self.__adapt_nutritional_values(meal_plan)
        user_maximum_calories = self.__maximum_allowed_to_consume_per_day(
            nutritional_plan, adapted_meal_plan
        )

        for meal in adapted_meal_plan:
            meal_items = self.__get_items_by_type_of_meal(meal, user_item_preference)
            meal_items.sort_values(by="score", ascending=False)
            for meal_date in date_list:
                try:
                    await self.nphm_interface.get_nutritional_plan_has_meal_by_date(
                        meal_date, nutritional_plan.id, meal["meals_of_plan_id"], db
                    )
                except NotFoundException:
                    with keep_nested_transaction(db):
                        new_nphm = await self.nphm_interface.create_nutritional_plan_has_meal(
                            meal_date, nutritional_plan.id, meal["meals_of_plan_id"], db
                        )

    @staticmethod
    def __get_date_range(nutritional_plan: NutritionalPlan) -> List[date]:
        first_date = min(meal.meal_date for meal in nutritional_plan.nutritional_plan_meals)
        return pd.date_range(start=first_date, end=nutritional_plan.validate_date).tolist()

    @staticmethod
    def __adapt_nutritional_values(types_of_meal_plan: List[dict]) -> List[dict]:
        keys = [
            "proteins_percentage",
            "lipids_percentage",
            "carbohydrates_percentage",
            "calories_percentage",
        ]

        plan_percentages = {key: sum(meal[key] for meal in types_of_meal_plan) for key in keys}
        num_meals = len(types_of_meal_plan)

        for key, value in plan_percentages.items():
            if value > 100:
                excess = value - 100
                for meal in types_of_meal_plan:
                    meal[key] -= excess / num_meals

        return types_of_meal_plan

    @staticmethod
    def __maximum_allowed_to_consume_per_day(
        nutritional_plan: NutritionalPlan, types_of_meal_plan: List[dict]
    ) -> dict:
        divisor = (
            nutritional_plan.period_limit.days
            if nutritional_plan.period_limit.days
            else 1 / len(types_of_meal_plan)
        )

        nutritional_limits = {
            "proteins_limit": nutritional_plan.proteins_limit,
            "lipids_limit": nutritional_plan.lipids_limit,
            "carbohydrates_limit": nutritional_plan.carbohydrates_limit,
            "calories_limit": nutritional_plan.calories_limit,
        }

        for nutrient, limit in nutritional_limits.items():
            nutritional_limits[nutrient] = limit / divisor

        return nutritional_limits

    @staticmethod
    def __get_items_by_type_of_meal(
        meal_of_plan: dict, user_item_preference: pd.DataFrame
    ) -> pd.DataFrame:
        return user_item_preference[
            user_item_preference["can_eat_at"].apply(lambda x: meal_of_plan["type_of_meal_id"] in x)
        ]
