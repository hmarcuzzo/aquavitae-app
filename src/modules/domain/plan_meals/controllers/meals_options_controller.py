from fastapi import APIRouter

from src.modules.domain.plan_meals.services.meals_options_service import MealsOptionsService

meals_options_router = APIRouter(tags=["Meals Options"], prefix="/meals-options")

meals_options_service = MealsOptionsService()
