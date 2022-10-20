from fastapi import APIRouter

from src.modules.domain.plan_meals.services.nutritional_plan_has_meal_service import (
    NutritionalPlanHasMealService,
)

nutritional_plan_has_meal_router = APIRouter(
    tags=["Nutritional Plan Has Meal"], prefix="/nutritional-plan-has-meal"
)

nutritional_plan_has_meal_service = NutritionalPlanHasMealService()
