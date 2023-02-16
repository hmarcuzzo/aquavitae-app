from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.modules.domain.recommendation_system.dto.user_preferences_table_dto import (
    DetailedUserPreferencesTable,
    SimplifiedUserPreferencesTable,
)
from src.modules.domain.recommendation_system.services.recommendation_system_service import (
    RecommendationSystemService,
)
from src.modules.infrastructure.database import get_db

rs_router = APIRouter(tags=["Recommendation System"], prefix="/recommendation-system")

rs_service = RecommendationSystemService()


@rs_router.post(
    "/complete-nutritional-plan",
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def complete_nutritional_plan(
    user_id: UUID,
    nutritional_plan_id: UUID,
    available: bool = True,
    force_reload: bool = False,
    database: Session = Depends(get_db),
) -> None:
    await rs_service.complete_nutritional_plan(
        str(user_id), str(nutritional_plan_id), available, force_reload, database
    )


@rs_router.get(
    "/food-preferences",
    response_model=List[SimplifiedUserPreferencesTable],
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def user_food_preferences(
    user_id: UUID,
    nutritional_plan_id: UUID,
    available: bool = True,
    force_reload: bool = False,
    database: Session = Depends(get_db),
) -> List[DetailedUserPreferencesTable]:
    return await rs_service.get_user_food_preferences(
        str(user_id), str(nutritional_plan_id), available, force_reload, database
    )
