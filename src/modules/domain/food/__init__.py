from fastapi import APIRouter

from .entities.food_entity import Food
from .controllers.food_controller import food_router

from .entities.food_category_entity import FoodCategory
from .controllers.food_category_controller import food_category_router

food_routers = APIRouter()
food_routers.include_router(food_router)
food_routers.include_router(food_category_router)

food_entities = [Food, FoodCategory]
