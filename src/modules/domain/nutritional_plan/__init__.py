from fastapi import APIRouter

from .entities.nutritional_plan_entity import NutritionalPlan
from .controllers.nutritional_plan_controller import nutritional_plan_router


nutritional_plan_routers = APIRouter()
nutritional_plan_routers.include_router(nutritional_plan_router)

nutritional_plan_entities = [NutritionalPlan]
