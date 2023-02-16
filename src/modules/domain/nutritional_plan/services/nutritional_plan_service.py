from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.nutritional_plan.repositories.nutritional_plan_repository import (
    NutritionalPlanRepository,
)


class NutritionalPlanService:
    def __init__(self):
        self.nutritional_plan_repository = NutritionalPlanRepository()

    # ---------------------- INTERFACE METHODS ----------------------
    async def find_one_nutritional_plan_by_id(
        self, nutritional_plan_id: str, db: Session
    ) -> Optional[NutritionalPlan]:
        nutritional_plan = await self.nutritional_plan_repository.find_one_or_fail(
            {
                "where": NutritionalPlan.id == nutritional_plan_id,
                "relations": ["nutritional_plan_meals"],
            },
            db,
        )

        return nutritional_plan
