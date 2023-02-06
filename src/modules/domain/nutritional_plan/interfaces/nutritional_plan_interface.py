from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.food.dto.food.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.nutritional_plan.services.nutritional_plan_service import (
    NutritionalPlanService,
)


class NutritionalPlanInterface:
    def __init__(self):
        self.nutritional_plan_service = NutritionalPlanService()

    async def get_nutritional_plan(
        self, nutritional_plan_id: str, db: Session
    ) -> Optional[FoodDto]:
        return await self.nutritional_plan_service.find_one_nutritional_plan_by_id(
            nutritional_plan_id, db
        )

    async def create_food(
        self,
        description: str,
        proteins: float,
        lipids: float,
        carbohydrates: float,
        energy_value: float,
        potassium: float,
        phosphorus: float,
        sodium: float,
        food_category_id: UUID,
        db: Session,
    ) -> Optional[FoodDto]:
        return await self.nutritional_plan_service.create_food(
            CreateFoodDto(
                **{
                    "description": description,
                    "proteins": proteins,
                    "lipids": lipids,
                    "carbohydrates": carbohydrates,
                    "energy_value": energy_value,
                    "potassium": potassium,
                    "phosphorus": phosphorus,
                    "sodium": sodium,
                    "food_category": food_category_id,
                }
            ),
            db,
        )

    async def get_all_food(self, db: Session) -> Optional[list[FoodDto]]:
        return await self.nutritional_plan_service.get_all_food(db)
