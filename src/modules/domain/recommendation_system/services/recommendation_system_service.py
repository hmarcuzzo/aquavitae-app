from typing import List
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session

from src.core.constants.enum.specificity_type import SpecificityTypes
from src.core.types.exceptions_type import BadRequestException
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.interfaces.food_category_interface import FoodCategoryInterface
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
        self.food_category_interface = FoodCategoryInterface()

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

        await self.__generate_food_preference_ranking(user_id, all_foods, db)

        if available:
            cant_consume_foods = [
                FoodDto(**item)
                for item in self.rs_repository.get_user_cant_consume_food_ids(
                    user_id, nutritional_plan_id, db
                )
            ]

    # ---------------------- PRIVATE METHODS ----------------------
    async def __generate_food_preference_ranking(
        self, user_id: str, all_foods: List[FoodDto], db_session: Session
    ):
        all_food_categories = pd.DataFrame.from_records(
            [
                food_category.__dict__
                for food_category in (
                    await self.food_category_interface.get_all_food_categories(db_session)
                )
            ]
        )
        user_preferences = self.rs_repository.get_user_food_preferences(user_id, db_session)
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
            all_food += RecommendationSystemService.__get_foods_from_category(children_category)
        return all_food + father.foods if father.foods else all_food

    @staticmethod
    def __define_score_by_preference_type(
        foods_dt: pd.DataFrame,
        food: pd.DataFrame,
        food_category: pd.DataFrame,
        foods_to_grade: List[Food],
        positive: bool = True,
    ) -> None:
        for food_same_category in foods_to_grade:
            if food_same_category.id == food["id"].iloc[0]:
                score = 50
            elif food_same_category.food_category_id == food_category["id"].iloc[0]:
                score = 25
            elif food_same_category.food_category.parent.id == food_category["parent"].iloc[0].id:
                score = 12
            else:
                score = 7

            RecommendationSystemService.__award_score(
                foods_dt, food_same_category.id, score, positive
            )

    def __award_score_by_consumption(
        self, db_session: Session, user_id: str, foods_dt: pd.DataFrame
    ) -> None:
        fatigued_food = self.rs_repository.get_fatigued_food_from_user(db_session, user_id, 30, 1)
        user_consumption = self.rs_repository.get_user_consumption_last_days(
            db_session, user_id, fatigued_food, 100
        )

        for food_id in fatigued_food:
            RecommendationSystemService.__award_score(foods_dt, food_id, 50, False)

    @staticmethod
    def __award_score(
        foods_dt: pd.DataFrame, food_id: UUID, score: int, positive: bool = True
    ) -> None:
        foods_dt.loc[foods_dt["id"] == food_id, "score"] += score if positive else -score
