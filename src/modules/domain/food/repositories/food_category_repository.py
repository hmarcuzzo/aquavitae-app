from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.infrastructure.database.base_repository import BaseRepository


class FoodCategoryRepository(BaseRepository[FoodCategory]):
    def __init__(self):
        super().__init__(FoodCategory)
