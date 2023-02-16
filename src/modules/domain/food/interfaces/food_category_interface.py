from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.domain.food.dto.food_category.create_food_category_dto import CreateFoodCategoryDto
from src.modules.domain.food.dto.food_category.food_category_dto import FoodCategoryDto
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.services.food_category_service import FoodCategoryService


class FoodCategoryInterface:
    def __init__(self):
        self.food_category_service = FoodCategoryService()

    async def find_one_category_by_description(
        self, description: str, db: Session
    ) -> Optional[FoodCategory]:
        return await self.food_category_service.find_one_category_by_description(description, db)

    async def create_category(
        self, description: str, level: int, parent: Union[UUID, None], db: Session
    ) -> Optional[FoodCategoryDto]:
        return await self.food_category_service.create_food_category(
            CreateFoodCategoryDto(
                **{"description": description, "level": level, "food_category": parent}
            ),
            db,
        )

    async def get_all_food_categories(self, db: Session) -> Optional[List[FoodCategory]]:
        return await self.food_category_service.get_all_food_categories(db)

    @staticmethod
    def get_all_foods_from_category(food_category: FoodCategory) -> List[Food]:
        all_food = []
        for children in food_category.children:
            all_food += FoodCategoryInterface.get_all_foods_from_category(children)

        return all_food + food_category.foods if food_category.foods else all_food
