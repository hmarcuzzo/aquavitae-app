from typing import Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.food.dto.food.create_food_dto import CreateFoodDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.domain.food.services.food_service import FoodService


class FoodInterface:
    def __init__(self):
        self.food_service = FoodService()

    async def find_one_food_by_description(
        self, description: str, db: Session
    ) -> Optional[FoodDto]:
        return await self.food_service.find_one_food_by_description(description, db)

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
        return await self.food_service.create_food(
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
