from fastapi import APIRouter

from src.modules.domain.plan_meals.services.meals_of_plan_service import MealsOfPlanService

meals_of_plan_router = APIRouter(tags=["Meals of Plan"], prefix="/meals-of-plan")

meals_of_plan_service = MealsOfPlanService()
