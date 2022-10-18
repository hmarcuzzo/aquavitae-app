from fastapi import APIRouter

from src.modules.domain.meal.services.food_can_eat_at_service import FoodCanEatAtService

food_cat_eat_at_router = APIRouter(tags=["Food Can Eat At"], prefix="/food-can-eat-at")

food_cat_eat_at_service = FoodCanEatAtService()
