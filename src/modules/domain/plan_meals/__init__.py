from fastapi import APIRouter

from .entities.meals_of_plan_entity import MealsOfPlan
from .controllers.meals_of_plan_controller import meals_of_plan_router

from .entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal

plan_meals_routers = APIRouter()
plan_meals_routers.include_router(meals_of_plan_router)

plan_meals_entities = [MealsOfPlan, NutritionalPlanHasMeal]
