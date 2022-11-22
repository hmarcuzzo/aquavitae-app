from fastapi import APIRouter

from src.modules.domain.nutritional_plan.services.nutritional_plan_service import (
    NutritionalPlanService,
)

nutritional_plan_router = APIRouter(tags=["Nutritional Plan"], prefix="/nutritional-plan")

nutritional_plan_service = NutritionalPlanService()
