from math import floor
from typing import List
from uuid import UUID

import pandas as pd
from cachetools import TTLCache
from sqlalchemy.orm import Session

from src.core.constants.enum.specificity_type import SpecificityTypes
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.interfaces.food_category_interface import FoodCategoryInterface
from src.modules.domain.food.interfaces.food_interface import FoodInterface
from src.modules.domain.nutritional_plan.interfaces.nutritional_plan_interface import (
    NutritionalPlanInterface,
)
from src.modules.domain.recommendation_system.dto.user_preferences_table_dto import (
    DetailedUserPreferencesTable,
)
from src.modules.domain.recommendation_system.repositories.recommendation_system_repository import (
    RecommendationSystemRepository,
)

all_food_cache = TTLCache(maxsize=1, ttl=60 * 60)
user_food_preference_cache = TTLCache(maxsize=100, ttl=60 * 60)


def all_foods_cache_key(db: Session):
    return f"all_foods_{db.get_bind().url.database}_{db.get_bind().dialect.name}"


class FindUserFoodPreferencesInterface:
    def __init__(self):
        self.rs_repository = RecommendationSystemRepository()
        self.food_interface = FoodInterface()
        self.nutritional_plan_interface = NutritionalPlanInterface()
        self.food_category_interface = FoodCategoryInterface()

        self.PERIOD_TO_FATIGUE = 30
        self.AMOUNT_TO_FATIGUE = 1
        self.PERIOD_TO_ANALYZE = 100
        self.PERCENTAGE_NEAR_FATIGUE = 0.9
        self.PERCENTAGE_FOR_IDENTIFICATION = 0.15

    # ----------------- PUBLIC METHODS ----------------- #
    async def get_user_food_preferences(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ) -> List[DetailedUserPreferencesTable]:
        all_foods = await self.__get_all_foods(db, force_reload)

        user_food_preference = await self.__generate_food_preference_ranking(user_id, all_foods, db)

        if available:
            cant_consume_foods = self.rs_repository.get_user_cant_consume_food_ids(
                user_id, nutritional_plan_id, db
            )

            for food in cant_consume_foods:
                user_food_preference = [
                    item for item in user_food_preference if item.id != food["food_id"]
                ]

        return user_food_preference

    # ----------------- PRIVATE METHODS ----------------- #
    async def __get_all_foods(self, db: Session, force_reload: bool = False):
        if force_reload or all_foods_cache_key(db) not in all_food_cache:
            all_foods = await self.food_interface.get_all_food(db)
            all_food_cache[all_foods_cache_key(db)] = all_foods
            return all_foods
        else:
            return all_food_cache[all_foods_cache_key(db)]

    async def __generate_food_preference_ranking(
        self, user_id: str, all_foods: List[FoodDto], db_session: Session
    ) -> List[DetailedUserPreferencesTable]:
        all_food_categories = pd.DataFrame.from_records(
            [
                food_category.__dict__
                for food_category in (
                    await self.food_category_interface.get_all_food_categories(db_session)
                )
            ]
        )
        user_preferences = self.rs_repository.get_user_food_preferences(user_id, db_session)

        hashable_key = (tuple(all_food_categories), tuple(user_preferences), tuple(all_foods))
        if user_food_preference_cache.get(hashable_key):
            return user_food_preference_cache[hashable_key]

        food_data = pd.DataFrame.from_records([food.dict() for food in all_foods])
        food_data["score"] = 0

        for index, food_preference in user_preferences.iterrows():
            current_food = food_data.loc[food_data["id"] == food_preference["food_id"]]
            current_category = all_food_categories.loc[
                all_food_categories["id"] == current_food["food_category"].iloc[0]
            ]

            root_category = self.__get_root_category(current_category)
            foods_to_grade = self.__get_foods_from_category(root_category)
            self.__award_score_by_preference(
                food_preference, food_data, current_food, current_category, foods_to_grade
            )

        self.__award_score_by_consumption(db_session, user_id, food_data)

        food_data.sort_values("score", ascending=False, inplace=True)
        result = [DetailedUserPreferencesTable(**food) for food in food_data.to_dict("records")]

        user_food_preference_cache[hashable_key] = result
        return result

    @staticmethod
    def __get_root_category(food_category: pd.DataFrame) -> FoodCategory:
        root_category = food_category["parent"].iloc[0]
        while root_category is not None:
            root_category = root_category.parent
            if root_category.parent is None:
                break

        return root_category

    def __award_score_by_preference(
        self,
        food_preference: pd.Series,
        foods_data_df: pd.DataFrame,
        food: pd.DataFrame,
        food_category: pd.DataFrame,
        foods_to_grade: List[Food],
    ) -> None:
        specificity_likes = (
            food_preference["specificity_type_description"]
            in SpecificityTypes.specificity_likes_consume()
        )
        specificity_doesnt_like = (
            food_preference["specificity_type_description"]
            in SpecificityTypes.specificity_doesnt_like_consume()
        )

        if specificity_likes:
            self.__define_score_by_preference_type(
                foods_data_df, food, food_category, foods_to_grade
            )
        elif specificity_doesnt_like:
            self.__define_score_by_preference_type(
                foods_data_df, food, food_category, foods_to_grade, False
            )

    @staticmethod
    def __get_foods_from_category(father: FoodCategory) -> List[Food]:
        all_food = []
        for children_category in father.children:
            all_food += FindUserFoodPreferencesInterface.__get_foods_from_category(
                children_category
            )
        return all_food + father.foods if father.foods else all_food

    @staticmethod
    def __define_score_by_preference_type(
        foods_dt: pd.DataFrame,
        food: pd.DataFrame,
        food_category: pd.DataFrame,
        foods_to_grade: List[Food],
        positive: bool = True,
    ) -> None:
        for food_to_grade in foods_to_grade:
            if food_to_grade.id == food["id"].iloc[0]:
                score = 50
            elif food_to_grade.food_category_id == food_category["id"].iloc[0]:
                score = 25
            elif food_to_grade.food_category.parent.id == food_category["parent"].iloc[0].id:
                score = 12
            else:
                score = 7

            if not positive:
                score *= -1

            FindUserFoodPreferencesInterface.__award_score(foods_dt, food_to_grade.id, score)

    def __award_score_by_consumption(
        self, db_session: Session, user_id: str, foods_dt: pd.DataFrame
    ) -> None:
        fatigued_food = self.rs_repository.get_fatigued_food_from_user(
            db_session, user_id, self.PERIOD_TO_FATIGUE, self.AMOUNT_TO_FATIGUE
        )
        user_consumption = self.rs_repository.get_user_consumption_last_days(
            db_session, user_id, fatigued_food, self.PERIOD_TO_ANALYZE
        )

        for food_id in fatigued_food:
            FindUserFoodPreferencesInterface.__award_score(foods_dt, food_id, -100)

        for food_id, food_amount in user_consumption:
            """It sets the score based on the amount consumed, if it's close to the amount of fatigue it receives
            fewer points to discourage its recommendation.
                If it's a little above the defined minimum amount it's understood that the user has some degree of
            identification with that food.
                And finally if it's below the minimum amount it's not possible to assume whether the user likes it
            or not, so a lower score is assigned. Lower than the balance point but higher than that of the foods
            close to fatigue, the intention is that this food is recommended to find out in the future whether the
            user likes it or not."""
            score = (
                10
                if food_amount >= floor(self.AMOUNT_TO_FATIGUE * self.PERCENTAGE_NEAR_FATIGUE)
                else 30
                if food_amount >= floor(self.AMOUNT_TO_FATIGUE * self.PERCENTAGE_FOR_IDENTIFICATION)
                else 20
            )

            FindUserFoodPreferencesInterface.__award_score(foods_dt, food_id, score)

    @staticmethod
    def __award_score(foods_dt: pd.DataFrame, food_id: UUID, score: int) -> None:
        foods_dt.loc[foods_dt["id"] == food_id, "score"] += score
