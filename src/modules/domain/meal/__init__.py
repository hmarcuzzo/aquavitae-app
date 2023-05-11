from fastapi import APIRouter

from .entities.type_of_meal_entity import TypeOfMeal
from .controllers.type_of_meal_controller import type_of_meal_router

from .entities.item_can_eat_at_entity import ItemCanEatAt

meal_routers = APIRouter()
meal_routers.include_router(type_of_meal_router)

meal_entities = [TypeOfMeal, ItemCanEatAt]
