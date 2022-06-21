from src.modules.infrastructure.database.base_repository import BaseRepository
from src.modules.domain.food.entities.food_entity import Food


class FoodRepository(BaseRepository[Food]):
    def __init__(self):
        super().__init__(Food)
