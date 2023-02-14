from datetime import date, timedelta
from typing import List, Optional
from uuid import UUID

import pandas as pd
from sqlalchemy import and_, func, null, or_
from sqlalchemy.orm import Session

from src.core.constants.enum.specificity_type import SpecificityTypes
from src.modules.domain.diary.entities.diary_entity import Diary
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.forbidden_foods.entities.forbidden_foods_entity import ForbiddenFoods
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.entities.item_has_food_entity import ItemHasFood
from src.modules.domain.meal.entities.type_of_meal_entity import TypeOfMeal
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.plan_meals.entities.meals_of_plan_entity import MealsOfPlan
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import (
    NutritionalPlanHasMeal,
)
from src.modules.domain.specificity.entities.specificity_entity import Specificity
from src.modules.domain.specificity.entities.specificity_type_entity import SpecificityType
from src.modules.infrastructure.user.entities.user_entity import User


class RecommendationSystemRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_user_cant_consume_food_ids(
        user_id: str, nutritional_plan_id: str, db: Session
    ) -> Optional[List[dict]]:
        query = (
            db.query(
                Food.id.label("food_id"),
                Food.description.label("food_description"),
                SpecificityType.description.label("specificity_type_description"),
            )
            .outerjoin(Specificity, Food.id == Specificity.food_id)
            .outerjoin(SpecificityType, Specificity.specificity_type_id == SpecificityType.id)
            .outerjoin(ForbiddenFoods, Food.id == ForbiddenFoods.food_id)
            .where(
                and_(
                    Food.deleted_at == null(),
                    Specificity.deleted_at == null(),
                    SpecificityType.deleted_at == null(),
                    ForbiddenFoods.deleted_at == null(),
                    or_(
                        and_(
                            Specificity.user_id == user_id,
                            SpecificityType.description.in_(
                                SpecificityTypes.specificity_forbidden_consume()
                            ),
                        ),
                        ForbiddenFoods.nutritional_plan_id == nutritional_plan_id,
                    ),
                )
            )
        )

        return [dict(row) for row in query.all()]

    @staticmethod
    def get_user_food_preferences(user_id: str, db: Session) -> Optional[pd.DataFrame]:
        query = (
            db.query(
                Food.id.label("food_id"),
                Food.description.label("food_description"),
                SpecificityType.description.label("specificity_type_description"),
            )
            .outerjoin(Specificity, Food.id == Specificity.food_id)
            .outerjoin(SpecificityType, Specificity.specificity_type_id == SpecificityType.id)
            .where(
                and_(
                    Specificity.user_id == user_id,
                    Specificity.deleted_at == null(),
                    Food.deleted_at == null(),
                    SpecificityType.deleted_at == null(),
                    SpecificityType.description.in_(
                        SpecificityTypes.specificity_preferences_consumption()
                    ),
                )
            )
        )

        return pd.DataFrame.from_records([dict(row) for row in query.all()])

    @staticmethod
    def get_user_consumption_last_days(
        db: Session, user_id: str, fatigued_food: List[UUID], days: int = 100
    ) -> Optional[List[dict]]:
        days_before = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

        query = (
            db.query(
                User.id.label("user_id"),
                Food.id.label("food_id"),
                func.count(Food.id).label("count"),
            )
            .outerjoin(NutritionalPlan, NutritionalPlan.user_id == User.id)
            .outerjoin(
                NutritionalPlanHasMeal,
                NutritionalPlanHasMeal.nutritional_plan_id == NutritionalPlan.id,
            )
            .outerjoin(Diary, Diary.nutritional_plan_has_meal_id == NutritionalPlanHasMeal.id)
            .outerjoin(Item, Item.id == Diary.item_id)
            .outerjoin(ItemHasFood, ItemHasFood.item_id == Item.id)
            .outerjoin(Food, Food.id == ItemHasFood.food_id)
            .where(
                and_(
                    NutritionalPlan.user_id == user_id,
                    NutritionalPlanHasMeal.meal_date >= days_before,
                    NutritionalPlan.deleted_at == null(),
                    NutritionalPlanHasMeal.deleted_at == null(),
                    Diary.deleted_at == null(),
                    Item.deleted_at == null(),
                    ItemHasFood.deleted_at == null(),
                    Food.deleted_at == null(),
                    Food.id.notin_(fatigued_food),
                )
            )
            .group_by(User.id, Food.id)
        )

        result = []
        for row in query.all():
            row_dict = dict(row)
            row_dict.pop("user_id")
            result.append(row_dict)

        return result

    @staticmethod
    def get_fatigued_food_from_user(
        db: Session, user_id: str, days: int = 30, amount_fatigue: int = 15
    ) -> Optional[List[UUID]]:
        days_before = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

        query = (
            db.query(
                User.id.label("user_id"),
                Food.id.label("food_id"),
            )
            .outerjoin(NutritionalPlan, NutritionalPlan.user_id == User.id)
            .outerjoin(
                NutritionalPlanHasMeal,
                NutritionalPlanHasMeal.nutritional_plan_id == NutritionalPlan.id,
            )
            .outerjoin(Diary, Diary.nutritional_plan_has_meal_id == NutritionalPlanHasMeal.id)
            .outerjoin(Item, Item.id == Diary.item_id)
            .outerjoin(ItemHasFood, ItemHasFood.item_id == Item.id)
            .outerjoin(Food, Food.id == ItemHasFood.food_id)
            .where(
                and_(
                    NutritionalPlan.user_id == user_id,
                    NutritionalPlanHasMeal.meal_date >= days_before,
                    NutritionalPlan.deleted_at == null(),
                    NutritionalPlanHasMeal.deleted_at == null(),
                    Diary.deleted_at == null(),
                    Item.deleted_at == null(),
                    ItemHasFood.deleted_at == null(),
                    Food.deleted_at == null(),
                )
            )
            .group_by(User.id, Food.id)
            .having(func.count(Food.id) >= amount_fatigue)
        )

        result = []
        for row in query.all():
            row_dict = dict(row)
            result.append(row_dict["food_id"])

        return result

    @staticmethod
    def get_types_of_meal_plan(nutritional_plan_id: str, db: Session) -> List[dict]:
        query = (
            db.query(
                NutritionalPlan.id.label("nutritional_plan_id"),
                TypeOfMeal.id.label("type_of_meal_id"),
                TypeOfMeal.calories_percentage.label("calories_percentage"),
                TypeOfMeal.lipids_percentage.label("lipids_percentage"),
                TypeOfMeal.carbohydrates_percentage.label("carbohydrates_percentage"),
                TypeOfMeal.proteins_percentage.label("proteins_percentage"),
                MealsOfPlan.start_time.label("start_time"),
                MealsOfPlan.end_time.label("end_time"),
            )
            .outerjoin(
                NutritionalPlanHasMeal,
                NutritionalPlanHasMeal.nutritional_plan_id == NutritionalPlan.id,
            )
            .outerjoin(MealsOfPlan, MealsOfPlan.id == NutritionalPlanHasMeal.meals_of_plan_id)
            .outerjoin(TypeOfMeal, TypeOfMeal.id == MealsOfPlan.type_of_meal_id)
            .where(
                and_(
                    NutritionalPlan.id == nutritional_plan_id,
                    NutritionalPlan.deleted_at == null(),
                    NutritionalPlanHasMeal.deleted_at == null(),
                    MealsOfPlan.deleted_at == null(),
                    TypeOfMeal.deleted_at == null(),
                )
            )
            .distinct()
        )

        return [dict(row) for row in query.all()]
