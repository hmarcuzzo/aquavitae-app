from fastapi import APIRouter

from src.modules.domain.forbidden_foods.services.forbidden_foods_service import (
    ForbiddenFoodsService,
)

forbidden_foods_router = APIRouter(tags=["Forbidden Foods"], prefix="/forbidden_foods")

forbidden_foods_service = ForbiddenFoodsService()
