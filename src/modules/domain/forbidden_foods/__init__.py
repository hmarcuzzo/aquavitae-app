from fastapi import APIRouter

from .controllers.forbidden_foods_controller import forbidden_foods_router
from .entities.forbidden_foods_entity import ForbiddenFoods

forbidden_foods_routers = APIRouter()
forbidden_foods_routers.include_router(forbidden_foods_router)

forbidden_foods_entities = [ForbiddenFoods]
