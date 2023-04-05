from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import date
from math import ceil
from random import randint
from typing import Dict, List
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session

from src.core.constants.default_values import (
    DEFAULT_AMOUNT_GRAMS,
    MAXIMUM_SERVING_AMOUNT,
    MINIMUM_SERVING_AMOUNT,
)
from src.core.types.exceptions_type import BadRequestException, NotFoundException
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.nutritional_plan.interfaces.nutritional_plan_interface import (
    NutritionalPlanInterface,
)
from src.modules.domain.plan_meals.interfaces.meals_options_interface import MealsOptionsInterface
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
        self.meals_options_interface = MealsOptionsInterface()

    # ----------------- PUBLIC METHODS ----------------- #
    async def complete_nutritional_plan(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ) -> pd.DataFrame:
        types_of_meal_plan = self.rs_repository.get_types_of_meal_plan(nutritional_plan_id, db)
        if len(types_of_meal_plan) == 1 and types_of_meal_plan[0]["type_of_meal_id"] is None:
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

        await self.__complete_nutritional_plan(
            nutritional_plan, user_items_preference, types_of_meal_plan, db
        )

        return user_items_preference.sort_values("score", ascending=False)

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
    ) -> None:
        nutrients = ["proteins", "lipids", "carbohydrates", "calories"]

        date_list = self.__get_date_range(nutritional_plan)
        adapted_meal_plan = self.__adapt_nutritional_values(meal_plan)
        maximum_calories_per_day = self.__maximum_allowed_to_consume_per_day(
            nutritional_plan, adapted_meal_plan, nutrients
        )

        for meal in adapted_meal_plan:
            meal_items = self.__get_items_by_type_of_meal(meal, user_item_preference)

            maximum_calories_in_meal = self.__get_maximum_calories_in_meal(
                maximum_calories_per_day, meal, nutrients
            )
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
                        await self.__suggest_meals(
                            new_nphm.id, meal_items, maximum_calories_in_meal, db
                        )
                    db.commit()

    @staticmethod
    def __get_date_range(nutritional_plan: NutritionalPlan) -> List[date]:
        first_date = min(meal.meal_date for meal in nutritional_plan.nutritional_plan_meals)
        return pd.date_range(start=first_date, end=nutritional_plan.validate_date).tolist()

    @staticmethod
    def __adapt_nutritional_values(types_of_meal_plan: List[dict]) -> List[dict]:
        plan_percentages = {
            "calories_percentage": sum(meal["calories_percentage"] for meal in types_of_meal_plan)
        }
        num_meals = len(types_of_meal_plan)

        for key, value in plan_percentages.items():
            if value > 100:
                excess = value - 100
                for meal in types_of_meal_plan:
                    meal[key] -= excess / num_meals

        return types_of_meal_plan

    @staticmethod
    def __maximum_allowed_to_consume_per_day(
        nutritional_plan: NutritionalPlan, types_of_meal_plan: List[dict], nutrients: List[str]
    ) -> dict:
        divisor = (
            nutritional_plan.period_limit.days
            if nutritional_plan.period_limit.days
            else 1 / len(types_of_meal_plan)
        )

        return {
            f"{nutrient}_limit": getattr(nutritional_plan, f"{nutrient}_limit") / divisor
            for nutrient in nutrients
        }

    @staticmethod
    def __get_items_by_type_of_meal(
        meal_of_plan: dict, user_item_preference: pd.DataFrame
    ) -> pd.DataFrame:
        return user_item_preference[
            user_item_preference["can_eat_at"].apply(lambda x: meal_of_plan["type_of_meal_id"] in x)
        ]

    async def __suggest_meals(
        self,
        nphm_id: UUID,
        meal_items: pd.DataFrame,
        maximum_calories_in_meal: dict,
        db: Session,
    ) -> None:
        meal_items = meal_items.sort_values("score", ascending=False)
        size = len(meal_items)

        splitted_meals = [
            meal_items[0 : ceil(size * 0.1)],
            meal_items[ceil(size * 0.1) : ceil(size * 0.3)],
            meal_items[ceil(size * 0.3) : ceil(size * 0.6)],
        ]

        for splitted_item in splitted_meals:
            if not len(splitted_item):
                continue

            index = randint(0, len(splitted_item) - 1)
            item = splitted_item.iloc[index]
            amount = CompleteNutritionalPlanInterface.__find_ideal_quantity(
                item, maximum_calories_in_meal
            )
            await self.meals_options_interface.create_meal_option(
                amount, True, item["id"], nphm_id, db
            )

    @staticmethod
    def __get_maximum_calories_in_meal(
        maximum_calories_per_day: dict, meal: dict, nutrients: List[str]
    ) -> dict:
        if "calories" in nutrients:
            nutrients.remove("calories")

        maximum_calories_in_meal = {
            "calories_limit": maximum_calories_per_day["calories_limit"]
            * (meal["calories_percentage"] / 100)
        }

        calories_limit = maximum_calories_in_meal["calories_limit"]
        for nutrient in nutrients:
            nutrient_percentage = meal[f"{nutrient}_percentage"] / 100
            maximum_calories_in_meal[f"{nutrient}_limit"] = calories_limit * nutrient_percentage

        return maximum_calories_in_meal

    @staticmethod
    def __find_ideal_quantity(item: pd.Series, meal: dict) -> float:
        # Set initial value and adjustment factor
        quantity, step = MAXIMUM_SERVING_AMOUNT, MINIMUM_SERVING_AMOUNT

        while True:
            # Calculates the amount of nutrients for the current quantity
            proteins, lipids, carbohydrates, energy = (
                item["proteins"] * quantity,
                item["lipids"] * quantity,
                item["carbohydrates"] * quantity,
                item["energy_value"] * quantity,
            )

            # Checks that the nutrients are within the allowed limits
            if (
                proteins <= meal["proteins_limit"]
                and lipids <= meal["lipids_limit"]
                and carbohydrates <= meal["carbohydrates_limit"]
                and energy <= meal["calories_limit"]
            ):
                return quantity

            # If they aren't, adjust the quantity to approach the limit
            if (
                proteins > meal["proteins_limit"]
                or lipids > meal["lipids_limit"]
                or carbohydrates > meal["carbohydrates_limit"]
                or energy > meal["calories_limit"]
            ):
                quantity -= step

            # Checks that the quantity is within limits
            if quantity < MINIMUM_SERVING_AMOUNT:
                return MINIMUM_SERVING_AMOUNT
