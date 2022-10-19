from fastapi import APIRouter

from .entities.nutritional_plan_entity import NutritionalPlan

# from .controllers.type_of_meal_controller import type_of_meal_router


nutritional_plan_routers = APIRouter()
# nutritional_plan_routers.include_router(food_cat_eat_at_router)

nutritional_plan_entities = [NutritionalPlan]
