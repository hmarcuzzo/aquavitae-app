from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.create_nutritional_plan_has_meal_dto import (
    CreateNutritionalPlanHasMealDto,
)
from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.nutritional_plan_has_meal_dto import (
    NutritionalPlanHasMealDto,
)
from src.modules.domain.plan_meals.services.nutritional_plan_has_meal_service import (
    NutritionalPlanHasMealService,
)


class NutritionalPlanHasMealInterface:
    def __init__(self):
        self.nphm_service = NutritionalPlanHasMealService()

    async def get_nutritional_plan_has_meal_by_date(
        self, meal_date: date, nutritional_plan_id: UUID, meal_of_plan_id: UUID, db: Session
    ) -> Optional[NutritionalPlanHasMealDto]:
        return await self.nphm_service.get_nutritional_plan_has_meal_by_date(
            meal_date, nutritional_plan_id, meal_of_plan_id, db
        )

    async def create_nutritional_plan_has_meal(
        self, meal_date: date, nutritional_plan_id: UUID, meal_of_plan_id: UUID, db: Session
    ) -> Optional[NutritionalPlanHasMealDto]:
        return await self.nphm_service.create_nutritional_plan_has_meal(
            CreateNutritionalPlanHasMealDto(
                **{
                    "meal_date": meal_date,
                    "nutritional_plan": nutritional_plan_id,
                    "meals_of_plan": meal_of_plan_id,
                }
            ),
            db,
        )
