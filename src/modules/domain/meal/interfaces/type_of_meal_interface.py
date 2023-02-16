from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.meal.dto.type_of_meal.create_type_of_meal_dto import CreateTypeOfMealDto
from src.modules.domain.meal.dto.type_of_meal.type_of_meal_dto import TypeOfMealDto
from src.modules.domain.meal.services.type_of_meal_service import TypeOfMealService


class TypeOfMealInterface:
    def __init__(self):
        self.type_of_meal_service = TypeOfMealService()

    async def find_one_type_of_meal_by_description(
        self, description: str, db: Session
    ) -> Optional[TypeOfMealDto]:
        return await self.type_of_meal_service.find_one_type_of_meal_by_description(description, db)

    async def create_type_of_meal(
        self,
        description: str,
        calories: float,
        lipids: float,
        proteins: float,
        carbohydrates: float,
        db: Session,
    ) -> Optional[TypeOfMealDto]:
        return await self.type_of_meal_service.create_type_of_meal(
            CreateTypeOfMealDto(
                **{
                    "description": description,
                    "calories_percentage": calories,
                    "lipids_percentage": lipids,
                    "proteins_percentage": proteins,
                    "carbohydrates_percentage": carbohydrates,
                }
            ),
            db,
        )
