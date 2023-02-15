from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.nutritional_plan.dto.nutritional_plan_dto import NutritionalPlanDto
from src.modules.domain.nutritional_plan.services.nutritional_plan_service import (
    NutritionalPlanService,
)


class NutritionalPlanInterface:
    def __init__(self):
        self.nutritional_plan_service = NutritionalPlanService()

    async def get_nutritional_plan(
        self, nutritional_plan_id: str, db: Session
    ) -> Optional[NutritionalPlanDto]:
        return await self.nutritional_plan_service.find_one_nutritional_plan_by_id(
            nutritional_plan_id, db
        )
