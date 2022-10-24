from fastapi import APIRouter

from src.modules.domain.meal.services.type_of_meal_service import TypeOfMealService

type_of_meal_router = APIRouter(tags=["Type of Meal"], prefix="/type-of-meal")

type_of_meal_service = TypeOfMealService()
