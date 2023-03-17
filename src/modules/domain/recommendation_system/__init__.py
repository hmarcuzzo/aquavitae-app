from fastapi import APIRouter

from src.modules.domain.recommendation_system.controllers.recommendation_system_controller import (
    rs_router,
)

rs_routers = APIRouter()
rs_routers.include_router(rs_router)
