from fastapi import APIRouter

from .entities.type_of_meal_entity import TypeOfMeal
from .controllers.type_of_meal_controller import type_of_meal_router

from .entities.food_can_eat_at_entity import FoodCanEatAt
from .controllers.food_can_eat_at_controller import food_cat_eat_at_router

meal_routers = APIRouter()
meal_routers.include_router(type_of_meal_router)
meal_routers.include_router(food_cat_eat_at_router)

meal_entities = [TypeOfMeal, FoodCanEatAt]
